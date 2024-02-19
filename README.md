# **WikiBuddy - Wikipedia and Nytimes powered chatbot**

<img width="1792" alt="image" src="https://github.com/asimx07/WikiBuddy/assets/57403912/0013321c-d4a9-4eaa-8152-1c6a4b84a9d5">

WikiBuddy is a chatbot powered by a Large Language Model and based on Retrieval Augmented Generation (RAG) techniques. It utilizes datasets from Wikipedia.org and Nytimes.com collected from the internet, integrating both retrieval and generation models. This approasch ensures that WikiBuddy delivers responses that are more accurate and relevant compared to traditional chatbots

# Techstack
### Model
- [TheBloke/Mistral-7B-Instruct-v0.2-GGUF (4bit)](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
### Framework
- [Langchain](https://www.langchain.com/)
- [Llama-cpp-python](https://python.langchain.com/docs/integrations/llms/llamacpp) 
### API
- [FastAPI](https://fastapi.tiangolo.com/)
### Vectorestore
- [FAISS-CPU](https://faiss.ai/index.html)
## UI
- [Gradio](https://www.gradio.app/)
## Monitoring 
- [Langsmith](https://docs.smith.langchain.com/)

# Running Locally 

This project is intended to run 4bit version of open source LLM Mistral 7b Instruct locally on CPU. To run this locally first clone the repo and install dependencies in `requirements.txt`
```
pip3 install --no-cache-dir --upgrade requirements.txt 
```

## Ingestion 

To create the embeddings and vector store first run `ingestion.py` script. This script creates embedding and stores in vectorestore. Once the indexes are created they are saved locally in `saved-index-faiss` folder. 

###Note: This script MUST run before running `main.py` and takes quite lot of time. Alternatively, to speed up you can download the already created indexed from here and paste them in root directory. This way you do not need to run this script first. 

## Inference 
Once the indexes are ready run 
```
python3 main.py 
```
This should on first run, downlaod the model and download locally too. From next time the model will be cached. Once the server is up and running it will be available on 

`http://127.0.0.1:8000` 

You can test the inference at by making `POST` request at `http://127.0.0.1:8000/chat` 

The template for json body is 
```json
{
  "query": "Who is Taylor Swift?"
}
```

## User Interface 


**The UI is created using Gradio and can be accessed at `http://127.0.0.1:8000/gradio`**



## Documentation 

The Swagger UI is available on `http://127.0.0.1:8000/gradio` 

<img width="1792" alt="image" src="https://github.com/asimx07/WikiBuddy/assets/57403912/9397fea4-72a3-4469-9824-3b15fc116b5b">



## Tracing, Telemetry, Analytics 

<img width="1792" alt="image" src="https://github.com/asimx07/WikiBuddy/assets/57403912/8684c3a5-679d-4c6c-8ae3-d91fa6871f45">


[Langsmith](https://docs.smith.langchain.com/) is used for logging, analytics, monitoring. Setting up Langsmith for monitoring is really simple. 

1. Create a free account
2. Create a project
3. Get API Key

In project root directory create a new file name `.env` and add these details and re-run the application. 

```
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
export LANGCHAIN_API_KEY="<LANGSMITH_API_KEY>"
export LANGCHAIN_PROJECT="<PROJECT NAME>"

```

