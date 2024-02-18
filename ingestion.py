import logging
import asyncio
import time
import sys
from pathlib import Path
from typing import List
import langchain
langchain.verbose = True
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import nest_asyncio

nest_asyncio.apply()


URL_TEXTFILES = ["wikilinks.txt","nytimes.txt"]


def setup_logging():
    """
    Configure logging to write both to console and a log file.
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler("ingestion.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def read_urls_from_file(filenames: List[str]) -> List[str]:
    """
    Read URLs from files and return them as a list.
    """
    urls = []
    for file in filenames:
        path = Path(file)
        if not path.is_file():
            logging.error(f"File {file} not found.")
            continue
        with open(file, 'r') as file:
            for line in file:
                url = line.strip()
                urls.append(url)
    print("TOTAL URLS TO LOAD: ",len(urls))
    return urls


def load_documents_from_urls(urls: List[str], splitter: RecursiveCharacterTextSplitter) -> List[str]:
    """
    Load documents from a list of URLs using WebBaseLoader and split them into chunks.
    """
    all_chunks = []
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            document = loader.aload()
            chunks = splitter.split_documents(document)
            all_chunks.extend(chunks)
            logging.info(f"Loaded {url}, {len(document)} pages, {len(chunks)} chunks")
        except Exception as e:
            logging.error(f"Error loading {url}: {e}")
    return all_chunks


async def ingest_and_save_embeddings(urls_files: str):
    """
    Ingest documents from URLs, embed them, and save to local storage.
    """
    try:
        
        all_urls = read_urls_from_file(urls_files)
        splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
        all_chunks = load_documents_from_urls(all_urls, splitter)

        if not all_chunks:
            logging.error("No documents were successfully loaded.")
            return

        logging.info("Embedding the documents...")

        embedding_model_id = "BAAI/bge-base-en-v1.5"
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_id)
        embeddings_db = await FAISS.afrom_documents(all_chunks, embeddings)
        logging.info("Ingestion complete. Saving now...")
        embeddings_db.save_local("saved-index-faiss")
        logging.info("Embeddings saved successfully.")
    except Exception as e:
        logging.error(f"Error during ingestion and saving: {e}")


if __name__ == "__main__":
    start_time = time.time()  
    setup_logging()
    urls_files = URL_TEXTFILES
    asyncio.run(ingest_and_save_embeddings(urls_files))
    end_time = time.time()  
    elapsed_time_seconds = end_time - start_time  
    elapsed_time_minutes = elapsed_time_seconds / 60  
    logging.info(f"Elapsed time: {elapsed_time_minutes:.2f} minutes")  # Log elapsed time in minutes

