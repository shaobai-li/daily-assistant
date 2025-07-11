from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

class Message(BaseModel):
    content: str

@app.post("/chat")
async def chat(request: Message):
    messages = [{"role": "user", "content": request.content}]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    return {"message": response.choices[0].message.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)