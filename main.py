from fastapi import FastAPI
from pydantic import BaseModel
import requests
app = FastAPI()
API_TOKEN = "PASTE_YOUR_HUGGINGFACE_TOKEN_HERE"
API_URL = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
class NewsArticle(BaseModel):
    text:str
def query_ai_model(text_to_analyze:str):
    headers = {"Authorization":f"Bearer {API_TOKEN}"}
    payload = {"inputs":text_to_analyze}

    print("--- DEBUG INFO ---")
    print(f"Calling URL: {API_URL}")

    response = requests.post(API_URL,headers=headers,json = payload)

    print(f"HF Response Status Code: {response.status_code}")
    print(f"HF Response Body: {response.text}") # We use .text to see the raw response, even if it's an error.
    print("--- END DEBUG INFO ---")

    if response.status_code == 200:
        return response.json()
    else:
        # If there was an error, return the error message.
        return {"error": f"API call failed with status code {response.status_code}", "details": response.text}

@app.get("/")
def read_root():
    return {"Hello" : "World"}
@app.post("/detect/")
def detect_news(article:NewsArticle):
   user_text = article.text
   print(f'Text received : {user_text}')

   ai_result = query_ai_model(user_text)
   print(f"AI result : {ai_result}")

   return {
       "original_text" : user_text,
       "AI_analysis" : ai_result
   }


 