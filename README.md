# AI/ML Legal Education System
- Project Description
This project builds an AI-powered legal education platform that processes legal texts, previous year documents, and YouTube transcripts to provide insights and support legal learning. It leverages large language models (LLMs), speech-to-text (STT), text-to-speech (TTS), and vector databases for retrieval-augmented generation (RAG).
File and Directory Structure
```bash
├── data/
│   ├── raw/
│   │   ├── previous_year_docs/      # Scraped legal documents
│   │   ├── youtube_transcripts/     # Transcribed YouTube videos
│   │   └── legal_texts/             # General legal reference materials
│   ├── processed/
│   │   ├── cleaned_text/            # Cleaned text data
│   │   │   ├── legal_texts/         # Cleaned legal texts
│   │   │   ├── previous_year_docs/  # Cleaned previous year docs
│   │   │   └── youtube_transcripts/ # Cleaned YouTube transcripts
│   │   ├── embeddings/              # Vector embeddings
│   │   └── metadata/                # Metadata for processed data
│   └── external/                    # Third-party datasets
├── notebooks/
│   ├── experiments/                 # Jupyter notebooks for experiments
│   │   ├── eda.ipynb
│   │   ├── model_training.ipynb
│   │   └── embedding_generation.ipynb
│   └── research/                    # Research and proof-of-concepts
├── src/
│   ├── app/                         # Front-end application
│   │   ├── streamlit_app.py         # Streamlit app entry point
│   │   ├── react_ui/                # React app source
│   │   └── utils/                   # App utilities
│   ├── data_ingestion/              # Data collection and processing
│   │   ├── web_scraper.py
│   │   ├── youtube_loader.py
│   │   ├── text_cleaner.py
│   │   └── __init__.py
│   ├── models/                      # Model definitions and weights
│   │   ├── llm/                     # LLM models
│   │   ├── stt/                     # STT models (e.g., Whisper)
│   │   ├── tts/                     # TTS models
│   │   ├── embeddings/              # Embedding models
│   │   └── __init__.py
│   ├── pipelines/                   # End-to-end workflows
│   │   ├── ingestion_pipeline.py
│   │   ├── retrieval_pipeline.py
│   │   └── __init__.py
│   ├── retrieval/                   # Retrieval logic
│   │   ├── vector_db/                   # Vector database handlers
│   │   ├── ranker.py
│   │   └── __init__.py
│   ├── utils/                       # General utilities
│   │   ├── text_processing.py
│   │   ├── audio_processing.py
│   │   ├── constants.py
│   │   └── __init__.py
│   └── tests/                       # Unit and integration tests
├── config/
│   ├── config.yaml                  # Project configurations
│   └── logging_config.yaml          # Logging settings
├── tests/                           # Top-level tests
├── .gitignore                       # Git ignore file
├── README.md                        # Project overview
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── setup.py                         # Python package setup
```
