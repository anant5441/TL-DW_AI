import streamlit as st
from streamlit import spinner
from applications import (
    extract_video_id,
    get_transcript, 
    translate_transcript,
    generate_notes,
    get_important_topics
)

st.set_page_config(
    page_title="TL;DW AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("🎬 TL;DW AI")
    st.markdown("### Too Long; Didn't Watch.")
    st.markdown("---")
    st.markdown("Transform any YouTube video into key topics, a podcast, or a chatbot.")
    st.markdown("### Input Details")
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    language = st.text_input("Video Language Code", placeholder="e.g., en, hi, es, fr", value="en")

    task_option = st.radio(
        "Choose what you want to generate:",
        ["Chat with Video", "Notes For You"]
    )

    submit_button = st.button("✨ Start Processing")
    st.markdown("---")
    # The "New Chat" button has been removed from here.

# --- Main Page ---
st.title("YouTube Content Synthesizer")
st.markdown("Paste a video link and select a task from the sidebar.")


# --- Processing Flow ---
if submit_button:
    if youtube_url and language:
        video_id= extract_video_id(youtube_url)
        if video_id:
            with spinner("Step 1/3 : Fetching Transcript....."):
                full_transcript= get_transcript(video_id, language)
                if language!="en":
                    with spinner("Step 1.5/3 : Translating Transcript into English, This may take few moments......"):
                        full_transcript= translate_transcript(full_transcript)

            if task_option=="Notes For You":
                with spinner("Step 2/3: Extracting important Topics..."):
                    import_topics= get_important_topics(full_transcript)
                    st.subheader("Important Topics")
                    st.write(import_topics)
                    st.markdown("---")

                with spinner("Step 3/3 : Generating Notes for you."):
                    notes= generate_notes(full_transcript)
                    st.subheader("Notes for you")
                    st.write(notes)

                st.success("Summary and Notes Generated.")
