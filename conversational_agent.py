# conversational_agent.py

import langchain
import pathlib
import logging
from langchain.chains import ConversationalRetrievalChain
from langchain_community.retrievers import WikipediaRetriever
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from huggingface_hub import hf_hub_download
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate

from langchain.memory import ConversationBufferMemory
langchain.debug = True 
from dotenv import load_dotenv
load_dotenv()

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
        index_path = pathlib.Path(__file__).parent / "saved-index-faiss"

        embeddings_db = FAISS.load_local(index_path, embeddings)
        
        custom_retriever = embeddings_db.as_retriever(search_kwargs={"k": 3})
        
        #community provided retrievers 

        #wkr = WikipediaRetriever(load_max_docs=3)
        #arr = ArxivRetriever(load_max_docs=3)
        #lotr = MergerRetriever(retrievers=[wkr, retriever])

        return custom_retriever

    def get_crc(self):
        llm = self.fetch_model()
        logging.info("\n Fetching Retriever.....")
        retriever = self.get_retriever()
        logging.info('\n ----------QA---------')

        # question_template = """You are an Wikipedia and New york Times AI Assistant.Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
        # At the end of standalone question add this 'Answer the question in English language.' If you do not know the answer reply with 'I am sorry, I dont have enough information'.
        # Chat History:
        # {chat_history}
        # Follow Up Input: {question}
        # Standalone question:
        # """

        
        # custom_standalone_question = PromptTemplate.from_template(question_template)


        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        crc = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory)

        return crc
