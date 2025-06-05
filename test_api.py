from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pyngrok import ngrok, conf
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple message model
class Message(BaseModel):
    text: str

# Simple response model
class Response(BaseModel):
    text: str

# Root endpoint
@app.post("/", response_model=Response)
@app.post("/api/messages", response_model=Response)
async def process_message(message: Message):
    if message.text.lower() == "hi":
        return Response(text="hello")
    return Response(text="I only respond to 'hi'")

# Startup logic
@app.on_event("startup")
async def startup_event():
    try:
        # Set ngrok authtoken directly
        conf.get_default().auth_token = ""
        
        public_url = ngrok.connect(8000)
        print(f"🌐 ngrok tunnel opened at: {public_url}")
    except Exception as e:
        print(f"⚠️ Failed to start ngrok: {e}")
        print(f"Server will be available locally at http://localhost:8000")

# Run app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 