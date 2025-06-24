from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
import os
import re

class TextCleaner:
    """Class to clean legal texts, previous year docs, and YouTube transcripts."""
    
    def __init__(self, base_path=r"C:\Users\bhati\OneDrive\Desktop\my_legal_ai_project\data"):
        """Initialize with base data path."""
        self.base_path = base_path
        self.paths = {
            "legal_texts": {
                "input": os.path.join(base_path, r"raw\legal_texts"),
                "output": os.path.join(base_path, r"processed\cleaned_text\legal_texts"),
                "type": "pdf"
            },
            "previous_year_docs": {
                "input": os.path.join(base_path, r"raw\previous_year_docs"),
                "output": os.path.join(base_path, r"processed\cleaned_text\previous_year_docs"),
                "type": "pdf"
            },
            "youtube_transcripts": {
                "input": os.path.join(base_path, r"raw\youtube_transcripts"),
                "output": os.path.join(base_path, r"processed\cleaned_text\youtube_transcripts"),
                "type": "txt"
            }
        }

    def clean_text(self, text):
        """Clean text: remove whitespace, headers/footers, case citations, section numbers, special chars."""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove headers/footers (e.g., "Page X of Y", copyright)
        text = re.sub(r'Page \d+ of \d+|\d{4} \w+ \d+|\(c\) \d{4}.*?$', '', text, flags=re.IGNORECASE)
        # Remove case citations (e.g., "Brown v. Board, 347 U.S. 483 (1954)", "[2020] 1 SCC 123")
        text = re.sub(r'[A-Za-z\s]+ v\.? [A-Za-z\s]+, \d+ [A-Z\.]+ \d+ \(\d{4}\)|\[\d{4}\] \d+ [A-Z]+ \d+', '', text, flags=re.IGNORECASE)
        # Remove section numbers (e.g., "Section 123", "Sec. 45A", "§ 19(1)(a)")
        text = re.sub(r'(Section|Sec\.|§)\s*\d+[A-Za-z]*\d*\s*(?:\([a-zA-Z0-9\s]*\))?', '', text, flags=re.IGNORECASE)
        # Remove special characters (keep alphanumeric, spaces, basic punctuation)
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        return text

    def process_files(self, input_path, output_path, file_type="pdf"):
        """Process files (PDF or text) from input_path, clean, and save to output_path."""
        os.makedirs(output_path, exist_ok=True)
        loader_cls = PyPDFLoader if file_type == "pdf" else TextLoader
        glob_pattern = "*.pdf" if file_type == "pdf" else "*.txt"
        
        loader = DirectoryLoader(path=input_path, glob=glob_pattern, loader_cls=loader_cls)
        
        try:
            docs = loader.load()  # Use load() for full PDF processing
            for doc in docs:
                print(f"Processing: {doc.metadata['source']}")
                cleaned_text = self.clean_text(doc.page_content)
                output_file = os.path.join(output_path, f"{os.path.basename(doc.metadata['source'])}.txt")
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(cleaned_text + "\n")
                print(f"Appended cleaned text to: {output_file}")
        except Exception as e:
            print(f"Error processing files in {input_path}: {e}")

    def clean_all_data(self):
        """Clean all data types: legal_texts, previous_year_docs, youtube_transcripts."""
        for data_type, config in self.paths.items():
            print(f"\nCleaning {data_type}...")
            self.process_files(config["input"], config["output"], config["type"])

if __name__ == "__main__":
    cleaner = TextCleaner()
    cleaner.clean_all_data()