from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA

# Initialize embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.from_texts(["Your health data context here"], embeddings)

def get_rag_insights(data):
    # Prepare the data
    context = "\n".join([f"Date: {d.date}, Routine: {d.data}, Analysis: {d.analysis}" for d in data])
    
    # Create a retrieval-based QA system
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    
    # Generate insights
    query = f"Based on this health data, provide insights and recommendations:\n{context}"
    response = qa.run(query)
    
    return response

