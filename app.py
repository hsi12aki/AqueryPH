import os
import fitz
import streamlit as st
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS #Facebook AI Similarity Search
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Setup LLM
@st.cache_resource
def load_llm():
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-large",
        tokenizer="google/flan-t5-large",
        device=1,
        max_new_tokens=512
    )
    return HuggingFacePipeline(pipeline=pipe)

llm = load_llm()

# Initialize chat history
if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

# Prompt Template
qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are a helpful assistant specializing in marine tourism in the Philippines.
    When the user asks for an itinerary or trip plan, respond in a structured timeline format.
    Use the information in the context below to create a detailed 3-day travel itinerary focused on 
    environmental and marine activities in the Philippines. 
    Include destinations, morning/afternoon activities, and make the plan readable and organized.

    Context: {context}
    Question: {question}
    Answer:
    """
)

# PDF loader
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Streamlit UI
#gradient background
gradient_bg = """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #3151C6, #00003D); 
        background-attachment: fixed;
    }
    </style>
"""
st.markdown(gradient_bg, unsafe_allow_html=True)


st.set_page_config(page_title="AqueryPH RAG", layout="centered")
st.title("AqueryPH RAG")

# Logo and Title
col1, col2 = st.columns([1, 4])  # Adjust column width ratios

with col1:
    st.image("assets/AQlogo.png", width=100)

with col2:
    st.markdown("## 🫧 AqueryPH - RAG App")
    st.markdown("### *Saving marine lives today!*")
    st.markdown(
        """
        Use Aquery PH to make the sea a better place.<br>
        Promoting responsible tourism and marine conservation.<br>
        """,
        unsafe_allow_html=True
    )

col1, col2 = st.columns([1, 4])  # Adjust column width ratios
with col1:
# File uploader
    uploaded_files = st.file_uploader("Upload PDF/s", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        all_text = ""

        with st.spinner("Reading and processing PDFs..."):
            for file in uploaded_files:
                all_text += extract_text_from_pdf(file) + "\n"

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=50
            )
            chunks = splitter.split_text(all_text)
            embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectordb = FAISS.from_texts(chunks, embedding=embedder)
            retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever,
                chain_type="stuff",
                return_source_documents=False,
                chain_type_kwargs={"prompt": qa_prompt}
            )
            st.success("PDFs processed. Ask your question.")
            st.session_state.qa_chain = qa_chain

        with st.expander("Extracted Text History"):
            st.write(all_text[:3000] + "..." if len(all_text) > 3000 else all_text)

with col2:

  # Example questions
    with st.expander("Example Questions You Can Try"):
        st.markdown("""
        - *where can I see the pawikans?*
        - *How can I book a trip to Siargao?*
        - *What are the best marine activities in Cebu?*
        - *Where are the conservation groups located at in the Philippines?*
        - *Why is there a need to have sustainable marine tourism in the Philippines?*
                    
        """)

  # Chat Interface
    if "qa_chain" in st.session_state:
        st.markdown("### How can we help you today?")
        question = st.text_input("Ask about your trip plans:", key="user_input")

        if question:
            with st.spinner("Generating answer..."):
                try:
                    result = st.session_state.qa_chain.run(question)
                    # Save to chat history
                    st.session_state.chat_history.append((question, result))
                    # Rerun to clear input box
                    st.session_state.pop("user_input", None)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        # Display Q&A history
        if st.session_state.chat_history:
            st.markdown("### Chat History")
            for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
                with st.container():
                    st.markdown(f"**Q{i}:** {q}")
                    st.markdown(f"**A{i}:** {a}")

    if st.session_state.chat_history:
        if st.button("Clear Chat History"):
            st.session_state.chat_history.clear()
            st.rerun()
