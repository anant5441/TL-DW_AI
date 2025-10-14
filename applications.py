from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.vectorstores import FAISS
from youtube_transcript_api.proxies import WebshareProxyConfig
from dotenv import load_dotenv
import streamlit as st
import time
import os
import re

load_dotenv()

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    st.error("Invalid YouTube URL. Please enter a valid URL.")
    return None

# function to get transcript from the video.
def get_transcript(video_id, language):
    yt_api= YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username="uovoumor",
            proxy_password="udk28jufv40l",
        )
    )
    try:
        transcript = yt_api.fetch(video_id, languages=[language])
        full_transcript = " ".join([i.text for i in transcript])
        time.sleep(10)
        return full_transcript
    except Exception as e:
        st.error(f"Could not retrieve a transcript for the video! This is most likely caused by:\n\n"
                    "Subtitles are disabled for this video or not available in the requested language.\n\n"
                    "If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, "
                    "please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues.")
        return None


# function to translate the transcript into english.
# initialize the gemini model
llm= ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.2
)    

#function to translate the transcript into english.
def translate_transcript(transcript):
    try:
        prompt=ChatPromptTemplate.from_template("""
        You are an expert translator with deep cultural and linguistic knowledge.
        I will provide you with a transcript. Your task is to translate it into English with absolute accuracy, preserving:
        - Full meaning and context (no omissions, no additions).
        - Tone and style (formal/informal, emotional/neutral as in original).
        - Nuances, idioms, and cultural expressions (adapt appropriately while keeping intent).
        - Speaker’s voice (same perspective, no rewriting into third-person).
        Do not summarize or simplify. The translation should read naturally in the target language but stay as close as possible to the original intent.

        Transcript:
        {transcript}
        """)

        #Runnables
        chain=prompt | llm

        #Run Chain
        response=chain.invoke({"transcript":transcript})

        return response.content
    
    except Exception as e:
        st.error(f"Error creating prompt: {e}")

#function to get important topics
def get_important_topics(transcript):
    try:
        prompt=ChatPromptTemplate.from_template("""
        You are an assistant that extracts the 5 most important topics discussed in a video transcript or summary.

                Rules:
                - Summarize into exactly 5 major points.
                - Each point should represent a key topic or concept, not small details.
                - Keep wording concise and focused on the technical content.
                - Do not phrase them as questions or opinions.
                - Output should be a numbered list.
                - show only points that are discussed in the transcript.
                Here is the transcript:
                {transcript}
        """)
        # Runnable chain
        chain = prompt | llm

        # Run chain
        response = chain.invoke({"transcript": transcript})

        return response.content

    except Exception as e:
        st.error(f"Error fething video {e}")


# FUNCTION TO GET NOTES FROM THE VIDEO
def generate_notes(transcript):
    try:
        prompt = ChatPromptTemplate.from_template("""
                You are an AI note-taker. Your task is to read the following YouTube video transcript 
                and produce well-structured, concise notes.

                ⚡ Requirements:
                - Present the output as **bulleted points**, grouped into clear sections.
                - Highlight key takeaways, important facts, and examples.
                - Use **short, clear sentences** (no long paragraphs).
                - If the transcript includes multiple themes, organize them under **subheadings**.
                - Do not add information that is not present in the transcript.

                Here is the transcript:
                {transcript}
                """)

        # Runnable chain
        chain = prompt | llm

        # Run chain
        response = chain.invoke({"transcript": transcript})

        return response.content

    except Exception as e:
        st.error(f"Error fething video {e}") 

# FUNCTION TO CREATE CHUNKS
def create_chunks(transcript):
    text_splitters= RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    doc= text_splitters.create_documents([transcript])
    return doc

# function to create embedding and store it into an vector space.
def create_vector_store(docs):
    embedding= GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", transport="grpc" )
    vector_store= FAISS.from_documents(docs, embedding)
    return vector_store


# RAG FUNCTION with Chat History Context
def rag_answer(question, vectorstore, chat_history=None):
    """
    Generate an answer based on the retrieved context and chat history.
    """
    # Step 1: Retrieve similar chunks from the vector store
    results = vectorstore.similarity_search(question, k=4)
    context_text = "\n".join([i.page_content for i in results])

    # Step 2: Format chat history (if any)
    history_text = ""
    if chat_history and len(chat_history) > 0:
        history_text = "\n".join(
            [f"User: {turn['user']}\nAssistant: {turn['assistant']}" for turn in chat_history]
        )

    # Step 3: Create a prompt that includes both context and history
    prompt = ChatPromptTemplate.from_template("""
    You are a kind, polite, and precise assistant helping the user based on a video transcript.

    Rules:
    - Use BOTH the retrieved video context and the previous chat history to understand the user’s intent.
    - Maintain conversational flow — be aware of what was said earlier.
    - Answer ONLY using the retrieved context or logically inferred information from it.
    - If the answer is not in the context or chat history, say:
      "I couldn’t find that information in the database. Could you please rephrase or ask something else?"
    - Keep your answers concise, clear, and friendly.

    ====== Retrieved Video Context ======
    {context}

    ====== Chat History ======
    {history}

    ====== User’s New Question ======
    {question}

    ====== Assistant’s Answer ======
    """)

    # Step 4: Run chain
    chain = prompt | llm
    response = chain.invoke({
        "context": context_text,
        "history": history_text,
        "question": question
    })

    return response.content
