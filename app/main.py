#uvicorn app.main:app --reload
 

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.routers import doc, auth, user

####
import os
import shutil

# Path to the folder
folder_path = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Test/PDF_Doc"

# Delete all files in the folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # Remove files or symbolic links
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Remove directories
    except Exception as e:
        print(f"Failed to delete {file_path}: {e}")
#delete content from txt file
# Path to the text file
txt_file_path = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Test/summary.txt"

# Clear content from the text file
with open(txt_file_path, 'w') as file:
    file.write("")

#Deleting all images
import os
import glob

# Path to the folder
folder_path = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Test/img2"

# File extensions to delete
image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff"]

# Delete all image files
for ext in image_extensions:
    files = glob.glob(os.path.join(folder_path, ext))
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Failed to delete {file}: {e}")


####

print("#" * 100)
print(settings.CLIENT_ORIGIN)

# Initialize FastAPI app
app = FastAPI()

# Serve static files (e.g., images, JavaScript, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS (Cross-Origin Resource Sharing) configuration
origins = [
    settings.CLIENT_ORIGIN,  # Use the CLIENT_ORIGIN for production environment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=[settings.CLIENT_ORIGIN],  # Allow requests from the frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["Authorization", "*"],  # Allow Authorization header explicitly
)


API_KEY = "CD78AF69D4789425F9278144F1121"

# API Key Verification Function
# async def verify_api_key(auth: str = Header(None)):
#     print(f"Received auth header: {auth}")  # Debugging: Print received header
#     if auth:
#         # Remove the Bearer prefix if it exists
#         auth = auth.replace("Bearer ", "")
#         print(f"Processed API key: {auth}")  # Debugging: Print processed key
#     else:
#         print("No auth header received")  # Debugging: If no header is received

#     if auth != API_KEY:
#         print("Invalid API key received")  # Debugging: Print when API key is invalid
#         raise HTTPException(status_code=401, detail="Invalid API key")

# Include the routers for authentication, user, and document endpoints
app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(doc.router, tags=['Docs'], prefix='/api',)
# app.include_router(doc.router, tags=['Docs'], prefix='/api', dependencies=[Depends(verify_api_key)])

# Health Check Endpoint
@app.get("/api/healthchecker")
def health_check():
    return {"message": "Welcome to Inlead ChatBot"}

# Root Endpoint (serves the main HTML page)
@app.get("/", response_class=HTMLResponse)
def read_root():
    # Read the index.html template file and return it with proper encoding
    with open("./templates/index.html", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)
