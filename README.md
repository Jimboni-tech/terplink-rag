# UMD Student Organization Recommendation System

A Retrieval-Augmented Generation (RAG) pipeline for discovering University of Maryland student organizations using semantic search and LLMs.

## Features

- **Automated Data Collection:** Scrapes and preprocesses 1,500+ UMD TerpLink organization pages using Selenium and Pandas.
- **Semantic Embedding:** Generates high-quality document embeddings with Hugging Face SentenceTransformers.
- **Vector Database:** Indexes embeddings in ChromaDB for fast, scalable similarity search.
- **RAG Search:** Uses cosine similarity and LLM prompting to recommend relevant student orgs based on user queries.
- **End-to-End Pipeline:** Modular scripts for scraping, cleaning, embedding, and querying.

## Project Structure

```
scripts/
  scrape-terplink.py         # Scrape org data from TerpLink
  data-preprocess.ipynb     # Clean and preprocess scraped data
  create-embeddings.py      # Generate embeddings and index in ChromaDB
  find-orgs.py              # Query system: retrieve and recommend orgs
  selenium_downloads/       # Temporary download folder for documents
```

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd terplink-rag
```

### 2. Install system dependencies

- **Python 3.10+**
- **Chrome** (for Selenium)
- **LibreOffice** (for .doc to .docx conversion)
  ```bash
  brew install --cask libreoffice
  ```

### 3. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install striprtf sentence-transformers tqdm
```

## Usage

### 1. Scrape and preprocess data

```bash
python scripts/scrape-terplink.py
# or run/step through scripts/data-preprocess.ipynb
```

### 2. Generate embeddings and index in ChromaDB

```bash
python scripts/create-embeddings.py
```

### 3. Query for relevant orgs

```bash
python scripts/find-orgs.py
```

## Example Query

Edit `find-orgs.py` to set your question:

```python
user_question = "I want to join orgs that do robotics and programming"
```

Run the script to print recommended orgs with context.

## Customization

- **Change embedding model:** Edit `create-embeddings.py` to use any SentenceTransformers model.
- **Tune prompt:** Edit the prompt template in `find-orgs.py` for your use case.
- **Scale up:** ChromaDB supports larger datasets and more advanced retrieval.

## Troubleshooting

- **Readonly database:** Delete or `chmod -R u+w data/chroma-data` if you see permission errors.
- **Selenium/Chrome issues:** Ensure Chrome and chromedriver are installed and compatible.
- **LibreOffice not found:** Install via Homebrew or your OS package manager.

## Credits

- [LangChain](https://github.com/langchain-ai/langchain)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [SentenceTransformers](https://www.sbert.net/)
- [Ollama](https://ollama.com/)

## License

MIT License
