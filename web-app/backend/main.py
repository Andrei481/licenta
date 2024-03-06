from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
from pydantic import BaseModel

app = FastAPI()

prompt = 'The capital of Germany is'
n = 1
temperature = 0.95
max_tokens = 200

origin = ["http://localhost:3000"]

# need to setup middleware in order to avoid CORS Error
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

class InferenceRequest(BaseModel):
    prompt: str
    n: int
    temperature: float
    max_tokens: int

@app.post("/inference")
async def run_inference(req_body: InferenceRequest):
    try:
        prompt = req_body.prompt
        n = req_body.n
        temperature = req_body.temperature
        max_tokens = req_body.max_tokens
        print("Received prompt: ", prompt)
        print("Received n: ", n)
        print("Received temperature: ", temperature)
        print("Received max_tokens: ", max_tokens)
        vllm_api_url = "http://0.0.0.0:8000/generate"
        data = {
            "prompt": prompt,
            "n" : n,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        vllm_response = requests.post(vllm_api_url, json=data)
        vllm_response.raise_for_status()
        return vllm_response.json()
    except requests.RequestException as err:
        print("Error communicating with the VLLM API: " + str(err))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)