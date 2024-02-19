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


@app.post("/chat")
async def completion(query: Validation, _empty):
    """
    Endpoint to process user queries and get responses.
    """
    try:
        global chat_history
        res = qa_chain.invoke({"question": query})
        
        #chat_history.append((query, res["answer"]))

        logging.info(f"Processed query: {query}")
        return res["answer"]
    except Exception as e:
        logging.error(f"Error processing query: {query}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

io =  gr.ChatInterface(
     fn=completion,
     chatbot=gr.Chatbot(height=400),
     textbox=gr.Textbox(placeholder="Ask Away! ", container=False, scale=6),
     title="WikiBuddy",
     description="Ask me any question",
     theme="soft",
     examples=["Who is David Beckham?", "Is Bitcoin Dead?", "What club does Christiano Ronaldo plays for?"],
     retry_btn=None,
     undo_btn="Delete Previous",
     clear_btn="Clear",
     analytics_enabled= True,
     fill_height=True
 )

app = gr.mount_gradio_app(app, io, path="/gradio")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



