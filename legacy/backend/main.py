from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from agents import RootAgent
import json
load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
assistant = RootAgent()

class Message(BaseModel):
    content: str

@app.post("/chat")
async def chat(request: Message):
    def event_stream():
        for chunk in assistant.recognize_intent(request.content):
            yield json.dumps({
                "message": chunk
            }) + "\n"
    return StreamingResponse(event_stream(), media_type="application/json")