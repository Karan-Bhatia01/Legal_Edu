from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv
import logging
import os

class RetrievalPipeline:
    """Handles query embedding, document retrieval, and LLM response generation."""
    
    def __init__(self, base_path=r"C:\Users\bhati\OneDrive\Desktop\my_legal_ai_project\data"):
        """Initialize with base path, embedding model, ChromaDB, and Groq client."""
        load_dotenv()  # Load .env file
        self.base_path = base_path
        self.logger = self._setup_logging()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path=os.path.join(base_path, r"vector_db"))
        self.collection = self.client.get_or_create_collection("legal_docs")
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file.")
        self.groq = Groq(api_key=groq_api_key)

    def _setup_logging(self):
        """Configure logging for pipeline execution."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(os.path.join(self.base_path, "retrieval_pipeline.log")),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def retrieve(self, query, n_results=10):
        """Embed query and retrieve top documents from ChromaDB."""
        try:
            self.logger.info(f"Processing query: {query}")
            query_embedding = self.model.encode([query])[0]
            results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
            self.logger.info(f"Retrieved {len(results['metadatas'][0])} documents")
            return results["metadatas"][0], results["documents"][0]
        except Exception as e:
            self.logger.error(f"Retrieval failed: {str(e)}")
            raise

    def generate_response(self, query, retrieved_docs):
        """Generate LLM response using Groq with retrieved documents as context."""
        try:
            context = "\n".join([doc["chunk"] for doc in retrieved_docs])
            prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer concisely:"
            self.logger.info("Generating LLM response...")
            response = self.groq.chat.completions.create(
                model="llama3-70b-8192",  # Updated to supported model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )
            answer = response.choices[0].message.content.strip()
            self.logger.info("Response generated successfully")
            return answer
        except Exception as e:
            self.logger.error(f"LLM response generation failed: {str(e)}")
            raise

    def run(self, query, n_results=10):
        """Execute full retrieval pipeline: retrieve documents and generate response."""
        self.logger.info("Starting retrieval pipeline...")
        retrieved_docs, documents = self.retrieve(query, n_results)
        response = self.generate_response(query, retrieved_docs)
        return {"query": query, "documents": documents, "response": response}

if __name__ == "__main__":
    pipeline = RetrievalPipeline()
    query = "Generate me curriculum to study indian constitution and Teach me step wise the main 10 lessons."
    result = pipeline.run(query)
    print(f"Query: {result['query']}")
    print(f"Retrieved Documents: {result['documents']}")
    print(f"Response: {result['response']}")