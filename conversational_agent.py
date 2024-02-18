# conversational_agent.py

import os
import langchain
import pathlib
import logging
from langchain.chains import ConversationalRetrievalChain
from langchain_community.retrievers import WikipediaRetriever
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from huggingface_hub import hf_hub_download
from langchain_community.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.memory import ConversationBufferMemory
langchain.debug = True 

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


class ConversationalAgent:
    def __init__(self):
        logging.basicConfig(filename='conversational_agent.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def fetch_model(self):
        HF_REPO_NAME = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
        HF_MODEL_NAME = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        REPO_MODELS_FOLDER = pathlib.Path(__file__).parent / "models"

        REPO_MODELS_FOLDER.mkdir(exist_ok=True)
        model_path = hf_hub_download(
            repo_id=HF_REPO_NAME, filename=HF_MODEL_NAME, local_dir=REPO_MODELS_FOLDER
        )

        model = LlamaCpp(
        model_path=model_path,
        temperature=0.3,
        max_tokens=250,
        top_k=2,
        verbose=True,  
        n_ctx=4096)
        print("Model Fetched")
        return model; 

    def get_retriever(self):
        embedding_model_id = "BAAI/bge-base-en-v1.5"
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_id)
        logging.info("Loading saved Embeddings.....")
        embeddings_db = FAISS.load_local("wikipedia-index-faiss", embeddings)
        custom_retriever = embeddings_db.as_retriever(search_kwargs={"k": 5})
        wkr = WikipediaRetriever(load_max_docs=3)
        #arr = ArxivRetriever(load_max_docs=3)
        #lotr = MergerRetriever(retrievers=[wkr, retriever])

        return custom_retriever

    def get_crc(self):
        llm = self.fetch_model()
        retriever = self.get_retriever()
        logging.info('\n ----------QA---------')
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        qa = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory)
        return qa
