from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import os
import pickle
import glob

class EmbeddingGenerator:
    """Class to split text, generate embeddings, and store them."""
    
    def __init__(self, base_path=r"C:\Users\bhati\OneDrive\Desktop\my_legal_ai_project\data"):
        self.base_path = base_path
        self.input_paths = {
            "legal_texts": os.path.join(base_path, r"processed\cleaned_text\legal_texts"),
            "previous_year_docs": os.path.join(base_path, r"processed\cleaned_text\previous_year_docs"),
            "youtube_transcripts": os.path.join(base_path, r"processed\cleaned_text\youtube_transcripts")
        }
        self.output_path = os.path.join(base_path, r"processed\embeddings")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight embedding model
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Adjust based on needs
            chunk_overlap=50  # Overlap for context
        )

    def load_text(self, input_path):
        """Load all text files from a directory."""
        texts = []
        for file_path in glob.glob(os.path.join(input_path, "*.txt")):
            with open(file_path, 'r', encoding='utf-8') as f:
                texts.append({"content": f.read(), "source": os.path.basename(file_path)})
        return texts

    def split_text(self, text):
        """Split text into chunks."""
        return self.text_splitter.split_text(text)

    def generate_embeddings(self, chunks):
        """Generate embeddings for text chunks."""
        return self.model.encode(chunks, show_progress_bar=True)

    def process_and_store_embeddings(self):
        """Process all text files, generate embeddings, and store them."""
        os.makedirs(self.output_path, exist_ok=True)
        
        for data_type, input_path in self.input_paths.items():
            print(f"\nProcessing {data_type}...")
            texts = self.load_text(input_path)
            if not texts:
                print(f"No texts found in {input_path}")
                continue
            
            all_embeddings = []
            metadata = []
            
            for text in texts:
                chunks = self.split_text(text["content"])
                if chunks:
                    embeddings = self.generate_embeddings(chunks)
                    all_embeddings.extend(embeddings)
                    metadata.extend([{"source": text["source"], "chunk": chunk} for chunk in chunks])
            
            # Save embeddings and metadata
            output_file = os.path.join(self.output_path, f"{data_type}_embeddings.pkl")
            with open(output_file, 'wb') as f:
                pickle.dump({"embeddings": all_embeddings, "metadata": metadata}, f)
            print(f"Saved embeddings to: {output_file}")

if __name__ == "__main__":
    generator = EmbeddingGenerator()
    generator.process_and_store_embeddings()