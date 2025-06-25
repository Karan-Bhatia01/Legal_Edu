import chromadb
import pickle
import os

def load_embeddings_to_chromadb(base_path=r"C:\Users\bhati\OneDrive\Desktop\my_legal_ai_project\data"):
    """Load embeddings from data/processed/embeddings/ into ChromaDB in batches."""
    client = chromadb.PersistentClient(path=os.path.join(base_path, r"vector_db"))
    collection = client.get_or_create_collection("legal_docs")
    batch_size = 5000  # Set to a safe value below ChromaDB's limit (5461)

    for data_type in ["legal_texts", "previous_year_docs", "youtube_transcripts"]:
        file_path = os.path.join(base_path, r"processed\embeddings", f"{data_type}_embeddings.pkl")
        if os.path.exists(file_path):
            print(f"Processing {file_path}...")
            with open(file_path, "rb") as f:
                data = pickle.load(f)
                embeddings = data["embeddings"]
                metadata = data["metadata"]
                ids = [f"{data_type}_{i}" for i in range(len(embeddings))]

                # Process in batches
                for i in range(0, len(embeddings), batch_size):
                    batch_embeddings = embeddings[i:i + batch_size]
                    batch_metadata = metadata[i:i + batch_size]
                    batch_ids = ids[i:i + batch_size]
                    try:
                        collection.add(
                            embeddings=batch_embeddings,
                            metadatas=batch_metadata,
                            ids=batch_ids
                        )
                        print(f"Added batch {i//batch_size + 1} for {data_type}")
                    except Exception as e:
                        print(f"Error adding batch for {data_type}: {str(e)}")
        else:
            print(f"No embeddings found for {data_type} at {file_path}")

if __name__ == "__main__":
    load_embeddings_to_chromadb()
