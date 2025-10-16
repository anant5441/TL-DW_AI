# 🎬 TL;DW AI 

**Too Long; Didn't Watch** - Transform any YouTube video into key topics, notes, or an interactive chatbot.

## 📋 Overview

TL;DW AI is a powerful application that leverages Google's Gemini AI to process YouTube videos and provide intelligent content summarization and interaction capabilities. Whether you want to quickly understand a video's key points or have a conversation about its content, this tool has you covered.

## ✨ Features

### 🎯 **Two Main Modes:**

1. **📝 Notes For You**
   - Extract 5 most important topics from the video
   - Generate well-structured, concise notes
   - Organize content into clear sections with bullet points
   - Highlight key takeaways and important facts

2. **💬 Chat with Video**
   - Interactive chatbot powered by RAG (Retrieval-Augmented Generation)
   - Ask questions about the video content
   - Maintains conversation context
   - Provides accurate answers based on video transcript

### 🌍 **Multi-language Support**
- Automatic transcript extraction in the video's original language
- Built-in translation to English using Gemini AI
- Support for any language with available YouTube transcripts

### 🔧 **Advanced AI Features**
- **Google Gemini 2.5 Flash Lite** for fast, accurate processing
- **FAISS vector database** for efficient similarity search
- **RAG implementation** with chat history context
- **Intelligent text chunking** for optimal processing
- **Streamlit Session State** for persistent chat history and vector store

## 📖 How to Use

1. **Enter YouTube URL**: Paste any YouTube video link in the sidebar
2. **Select Language**: Choose the video's language code (e.g., 'en', 'hi', 'es', 'fr')
3. **Choose Task**: Select between "Notes For You" or "Chat with Video"
4. **Click "Start Processing"**: The app will:
   - Extract the video transcript
   - Translate to English (if needed)
   - Process according to your selected task

### For Notes Mode:
- Get 5 key topics automatically extracted
- Receive structured notes with bullet points
- Content organized into clear sections

### For Chat Mode:
- Start asking questions about the video
- Get contextual answers based on the transcript
- Maintain conversation flow with chat history
- **Persistent chat sessions** - your conversation history is saved during the session
- **Context-aware responses** - AI remembers previous questions and answers

## 🛠️ Technical Architecture

### Core Components

- **`app.py`**: Main Streamlit application with UI and workflow
- **`applications.py`**: Core processing functions and AI integrations

### Session State Management

The application uses **Streamlit's session state** to maintain persistent data across user interactions:

- **`st.session_state.vector_store`**: Stores the FAISS vector database for the current video
- **`st.session_state.messages`**: Maintains the complete chat history as a list of message objects
- **Chat History Structure**: Each message contains:
  ```python
  {
      'role': 'user' or 'assistant',
      'content': 'message content'
  }
  ```

**Key Benefits:**
- **Persistent Conversations**: Chat history persists throughout the session
- **Context Preservation**: RAG system uses previous Q&A pairs for better context
- **Efficient Processing**: Vector store is created once and reused for all questions
- **Memory Management**: Session data is automatically cleared when the session ends

### Key Functions

- `extract_video_id()`: Extracts video ID from YouTube URLs
- `get_transcript()`: Fetches video transcripts using YouTube API
- `translate_transcript()`: Translates non-English transcripts
- `get_important_topics()`: Extracts key topics using AI
- `generate_notes()`: Creates structured notes from transcript
- `create_chunks()`: Splits transcript for vector processing
- `create_vector_store()`: Creates FAISS vector database
- `rag_answer()`: Powers the chatbot with RAG capabilities and chat history context

### Dependencies

- **Streamlit**: Web application framework
- **Google Generative AI**: Gemini model integration
- **YouTube Transcript API**: Video transcript extraction
- **LangChain**: AI framework for prompt management
- **FAISS**: Vector similarity search
- **Python-dotenv**: Environment variable management

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google AI API key for Gemini access

### Proxy Configuration
The app includes proxy configuration for YouTube transcript access. Update the proxy credentials in `applications.py` if needed:
```python
proxy_username="your_proxy_username"
proxy_password="your_proxy_password"
```


## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Common Issues

1. **"Could not retrieve transcript"**
   - Ensure the video has subtitles/transcripts enabled
   - Check if the language code is correct
   - Some videos may not have transcripts available

2. **API Key Issues**
   - Verify your Google AI API key is correct
   - Ensure the API key has proper permissions
   - Check if you have sufficient API quota

3. **Proxy Connection Issues**
   - Update proxy credentials if needed
   - Check proxy server availability

## 🔮 Future Enhancements

- [ ] Support for multiple video formats
- [ ] Batch processing capabilities
- [ ] Export notes to various formats (PDF, DOCX)
- [ ] Audio generation from notes
- [ ] Video chapter analysis
- [ ] Multi-video comparison features


**Made with ❤️ using Streamlit and Google Gemini AI**
