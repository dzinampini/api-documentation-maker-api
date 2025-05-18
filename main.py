from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import json
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define a Pydantic model for the POST request body
class Item(BaseModel):
    link: str
    version: str
    code: Optional[str] = Field(
        None,
        title="Python Code",
        description="Python Code which you wish to infer"
    )

# POST endpoint
@app.post("/infer_bert")
def create_item(item: Item):
    # print(item.link)
    open_ai_api_key = 'sk-proj-CGuX320UhPBU3Ch7i4EFT3BlbkFJ79Pc6ykL6xXDagPQC0a3'
    

    client = OpenAI(api_key=open_ai_api_key)

    # python_code = """
    # @app.get('/')
    # def read_root():
    #     return {'message': 'Welcome to the FastAPI demo!'}

    # # GET endpoint
    # @app.get('/sample')
    # def send_sample():
    #     try:
    #         file_path = os.path.join(os.path.dirname(__file__), 'example-api.json')
    #         with open(file_path, 'r') as file:
    #             data = json.load(file)
    #         return JSONResponse(content=data)
    #     except FileNotFoundError:
    #         return {'error': 'example-api.json file not found'}
    #     except json.JSONDecodeError:
    #         return {'error': 'Invalid JSON format in example-api.json'}
    # """
    python_code = item.code
    print(python_code)

    instruction = """From this given Python code for an API, may you extract for me the endpoint urls. Under each endpoint url, identify the methods. The get the payload for each method as well as responses that will be sent out. 
    I need the response in the following json format. 
    { /endpoint: { method: { description: string, requestBody: { content: {} }, responses: { responsecode: { decription: string, content: { }}}}} }"""

    response = client.responses.create(
        model="gpt-4.1",
        input=python_code + " " + instruction
    )

    # print(response.output_text)

    output_text = response.output_text  # Assuming this contains the response with ```json ... ```

    # Extract JSON part between ```json and ```
    json_str = output_text.split('```json')[1].split('```')[0].strip()
    # print(json_str)

    data = json.loads(json_str)
    cleaned_json = json.dumps(data, indent=2)
    print(cleaned_json)


    found_paths = cleaned_json

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