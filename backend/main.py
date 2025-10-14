from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from agents import RootAgent

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
assistant = RootAgent()

class Message(BaseModel):
    content: str

@app.post("/chat")
async def chat(request: Message):
    response = assistant.generate_response(request.content)
    return {"message": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)