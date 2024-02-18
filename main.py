# main.py

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import logging
from conversational_agent import ConversationalAgent
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

qa_chain = ConversationalAgent().get_crc()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, tighten this in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

chat_history = []

class Validation(BaseModel):
    """
    Pydantic BaseModel for input validation.
    """
    query: str


@app.get("/")
async def health_check():
    """
    Endpoint for health check.
    """
    return {"status": "Service is up and running!"}


@app.post("/openAiChat")
async def completion(query: Validation, _empty:str):
    """
    Endpoint to process user queries and get responses.
    """
    try:
        global chat_history
        res = qa_chain.invoke({"question": query})
      #  chat_history.append((query, res["answer"]))
        logging.info(f"Processed query: {query}")
        return res["answer"]
    except Exception as e:
        logging.error(f"Error processing query: {query}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
def vote(data: gr.LikeData):
    if data.liked:
        print(data.value)
    else:
        print(data)

io =  gr.ChatInterface(
     fn=completion,
     chatbot=gr.Chatbot(height=400),
     textbox=gr.Textbox(placeholder="Ask Away! ", container=False, scale=6),
     title="wiki-chat-pedia",
     description="Ask me any question",
     theme="soft",
     examples=["Who is David Beckham?", "Is Bitcoin Dead?", "What club does Christiano Ronaldo plays for?"],
     retry_btn=None,
     undo_btn="Delete Previous",
     clear_btn="Clear",
     analytics_enabled= True,
     

 )
app = gr.mount_gradio_app(app, io, path="/gradio")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



# SOME FINDINGS: 

# One problem: If the question is not follow up then a new tree starts
# However since the old info is in chat_history "stand alone question" 
# sometimes gets generated because it misunderstands the context 
# One way to solve this is flush the chat_history once conversation is over
# that's not optimal because the new topic could be related to older topic
# The other way is to Skip the standalone question generation if the question is
# not follow up quesiton. 
# Another Problem: is that includes chat history into request
#  which gets out of context window if long enough 
#  to solve both issues one tacky approach could be to flush
#  memory after 5 requests. This will include long term memory
#  loss though. 
# Note ConversationtalRetrievelChain does condense the history 
# so summarizing the chat history after few queries doesn't work 
# that efficiently with Langchain. 
#This doesn't work if I have to use the return_source_document, So I have created my own logic
#of saving chat history in main.py
#memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
