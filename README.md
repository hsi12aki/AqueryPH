# 🫧 AqueryPH °:•.🐠*.•🪸.•:°
*Saving marine lives today!*

![AqueryGIF](https://github.com/user-attachments/assets/48a3fd6a-531c-4d72-b685-ca3627c72724)

***AqueryPH*** is a Langchain-based RAG App that helps tourist to learn more <br>
about the marine ecosystem of the Philippines and help them navigate <br>
where to go for their trip to the Philippines. <br>
This app uses Streamlit for the UI.

<a href="https://aqueryph-rag-finals.streamlit.app/"> AqueryPH RAG App Streamlit </a>

⏏ Deployed version here ⏏

## ⚓ About the project ⚓
This project uses digital technology, especially Artificial Intelligence (AI), to tackle the challenges of responsible tourism and its effects on marine life in the Philippines. As tourism grows, it is important to reduce its harmful impacts on delicate marine ecosystems. We are developing an easy-to-use app that employs a modified Retrieval-Augmented Generation (RAG) model to gather and share important information about responsible tourism practices.


The app will help users quickly find tasks and data related to responsible tourism activities, making it a useful tool for both travelers and local communities. By using AI, the app will improve user experience and encourage sustainable practices that protect marine environments. It will provide links to conservation organizations, educational resources, and facts about how responsible tourism can benefit marine life, ensuring that users can make informed choices that support ecosystem health.

## ⚓ Technologies used ⚓
- Streamlit UI
- Langchain
- HuggingFace Transformers
- google/flan-t5-large
- Facebook AI Similarity Search (FAISS)
- PyMuPDF
- dotenv

## ⚓ Installation instructions ⚓
- Get a free API key from https://huggingface.co/
- Then, create a .env file
```
# .env file
HF_API_KEY=your_api_key_here
```
- In the terminal, clone the repository
```
git clone https://github.com/hsi12aki/AqueryPH.git
```
- Install requirements
```
pip install -r requirements.txt
```
- Run the app
```
streamlit run app.py
```

## ⚓ How it works ⚓

### ✦ Upload PDF
 - ***AqueryPH*** reads the documents about Marine life related information and conservation groups using `PyMuPDF`.

### ✦ Read into Chunks
 - The extracted text is divided into smaller chunks using LangChain's `RecursiveCharacterTextSplitter`.
```
chunk_size=300,
chunk_overlap=50
```
### ✦ Convert Chunks to Embeddings
 - Text chunks is converted into a numerical vector (an embedding) using the embedding model from HuggingFace, `all-MiniLM-L6-v2`.
 - 
### ✦ Store in FAISS Vector Store
 - The generated embeddings are stored in the FAISS index. This special database is highly optimized for finding the most similar vectors to a given query vector, which is how the app finds relevant information.

### ✦ Ask Questions

 - The user types a question. The app:

    - converts the user's query into an embedding.
    - FAISS is used to find the text chunks with embedding most similar to the questions embedding.
    - Relevant chunks are combined with the original questions and sent to the LLM, `flan-t5-large`. The script uses a custom prompt to guide the LLM’s response.
    - The LLM generates an answer based on the provided context and question, which is then displayed to the user.


## ⚓ Screenshots of the app ⚓

<img width="1912" height="990" alt="Screenshot 2025-07-30 203837" src="https://github.com/user-attachments/assets/80c5bf00-a427-46a0-a755-4f37968a1c10" />

<img width="1915" height="990" alt="Screenshot 2025-07-30 204042" src="https://github.com/user-attachments/assets/fa65915c-4f69-4707-851c-cb08aa2ebdb4" />

## ⚓ Group members and Contributions ⚓

<table>
  <tr>
    <th> <h3> Group members </h3> </th>
    <th> <h3> Contributions </h3> </th>
  </tr>
  <tr>
    <td> Denise Alcazar </td>
    <td> App Architecture, App Coding, Data Gathering, Troubleshooting, Readme.md Write-up, Github Pushing, Documentation </td>
  </tr>
  <tr>
    <td> Hazel Damasco </td>
    <td> Powerpoint, Readme.md Write-up, App Prototype </td>
  </tr>
  <tr>
    <td> Kaelynn Sianghio </td>
    <td> Leader, Abstract, Statement of the Problem, Troubleshooting, Data Gathering, App Prototype, Documentation </td>
  </tr>
</table>

