# API Documentation Editor Inference API
... 


## First Time Install and Running 
navigate into directory where you wnat to store project 
cd path\to\your\project

create a virtual environment 
python -m venv venv

activate environment 
venv\Scripts\activate

git clone <github_repository of api> api_project_clone_folder 

navigate into folder with cloned project 
cd <api_project_clone_folder>

pip install uvicorn
pip install fastapi 



run 
uvicorn main:app --reload 

test if running with visiting url localhost:8000/ or 127.0.0.1:8000/ (optional)

## Running 
navigate into directory where you cloned project in and where you created virtua environment (you can ski this if its already happening on terminal)
cd path\to\your\project

activate environment 
venv\Scripts\activate

navigate into folder with cloned project 
cd <api_project_clone_folder>

run 
uvicorn main:app --reload 

test if running with visiting url localhost:8000/ or 127.0.0.1:8000/ (optional)

## Deactivating Environment 
in case you no longer need it (environment)
deactivate
 

## In case model fails to load 
### Common Issue 1 - Missing Token Files 
1. Download the tokenizer files from base model (e.g., distilbert-base-uncased):
Drag these files from ./temp_tokenizer/:
tokenizer_config.json
vocab.txt
special_tokens_map.json
tokenizer.json 

2. Upload files manually to your Hugging Face repo:

Go to model repository on Hugging face  

Click "Add file" → "Upload files"


### Common Issue 2 - Missing Token Files 
Computer recognises localhost:5000/ not 127.0.0.1:5000/ or vise versa

### Common Issue 3 - Port number issues 
Check assigned port number if it matches 5000. 
check from cmd 

