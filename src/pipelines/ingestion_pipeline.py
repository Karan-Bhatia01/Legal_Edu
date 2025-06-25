from src.data_ingestion.text_cleaner import TextCleaner
from notebooks.experiments.embedding_generation import EmbeddingGenerator
import logging
import os

class IngestionPipeline:
    """Orchestrates data ingestion: cleaning raw data and generating embeddings."""
    
    def __init__(self, base_path=r"C:\Users\bhati\OneDrive\Desktop\my_legal_ai_project\data"):
        """Initialize with base data path and set up logging."""
        self.base_path = base_path
        self.logger = self._setup_logging()
        self.text_cleaner = TextCleaner(base_path)
        self.embedding_generator = EmbeddingGenerator(base_path)

    def _setup_logging(self):
        """Configure logging for pipeline execution."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(os.path.join(self.base_path, "ingestion_pipeline.log")),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def run(self):
        """Execute the full ingestion pipeline."""
        self.logger.info("Starting ingestion pipeline...")
        
        try:
            # Step 1: Clean raw data
            self.logger.info("Cleaning raw data...")
            self.text_cleaner.clean_all_data()
            self.logger.info("Data cleaning completed.")
            
            # Step 2: Generate embeddings
            self.logger.info("Generating embeddings...")
            self.embedding_generator.process_and_store_embeddings()
            self.logger.info("Embedding generation completed.")
            
            self.logger.info("Ingestion pipeline completed successfully.")
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise
