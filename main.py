from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import json
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize model once at startup
try:
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained("dzinampini/api_endpoint_extractor")
    model = AutoModelForSeq2SeqLM.from_pretrained("dzinampini/api_endpoint_extractor")
    model_loaded = True
    print("Model loaded successfully")
except Exception as e:
    model_loaded = False
    model_load_error = str(e)
    print(f"Model loading failed: {model_load_error}")

# Define a Pydantic model for the POST request body
class Item(BaseModel):
    link: str
    version: str
    code: Optional[str] = Field(
        None,
        title="Python Code",
        description="Python Code which you wish to infer"
    )

def extract_api_info(code_text: str):
    inputs = tokenizer(code_text, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=512)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded


# POST endpoint
@app.post("/infer_bert")
def create_item(item: Item):
    if not model_loaded:
        raise HTTPException(status_code=500, detail="Model not loaded")

    code_text = item.code or ""

    try:
        result = extract_api_info(code_text)
        result_json = json.loads(result)  
    except json.JSONDecodeError:
        result_json = {"error": "Model output is not valid JSON", "raw_output": result}

    return result_json
    
    python_code = item.code
    

    found_paths = []
    return found_paths



# GET endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI demo!"}

# GET endpoint
@app.get("/sample")
def send_sample():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "example-api.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        return JSONResponse(content=data)
    except FileNotFoundError:
        return {"error": "example-api.json file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in example-api.json"}


# uvicorn main:app --reload