#Install necessary packages
import os
import base64
from pathlib import Path
import uuid
import datetime
#from dotenv import load_dotenv  # Import to load .env variables
from langchain_core.messages import HumanMessage
#from langchain.schema import HumanMessage
#from langchain.chat_models import HumanMessage


#from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
#from langchain.chat_models import ChatOpenAI
from PIL import Image

# Load API keys and environment variables from .env file
#load_dotenv()

# Check for the OPENAI_API_KEY in the .env file
#api_key = os.getenv("OPENAI_API_KEY")
api_key="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"
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add it to continue.")
os.environ["OPENAI_API_KEY"] = api_key

# Set project-specific environment variables
uid = uuid.uuid4().hex[:6]
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
project_name = f"openai_image_summarization_{current_time}"
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = project_name
# os.environ["LANGCHAIN_API_KEY"] = "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"  # Replace with your actual key
LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="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"
LANGSMITH_PROJECT="chatbot"
OPENAI_API_KEY="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"

def encode_image_to_base64(image_path):
    """Encode image to base64 string."""
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found at {image_path}")

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/{image_path.suffix[1:]};base64,{base64_image}"


def display_image(image_path):
    """Display an image in the terminal using PIL."""
    try:
        img = Image.open(image_path)
        # Uncomment below to show the image
        # img.show()
    except Exception as e:
        print(f"Error displaying image: {e}")


def image_summarize(prompt, image_data_url):
    """Make image summary"""
    chat = ChatOpenAI(model="gpt-4-turbo", max_tokens=1024)

    # Create the message payload
    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",  # API expects 'image_url'
                        "image_url": {"url": image_data_url},
                    },
                ]
            )
        ]
    )
    return msg.content


if __name__ == "__main__":
    # Input: Folder containing images
    folder_path = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Test/img2"  # Replace with your folder path
    summary_file_path = "summary.txt"  # File to save summaries

    try:
        # List all image files in the folder
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        image_files = list(folder.glob("*.jpeg")) + list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
        if not image_files:
            raise FileNotFoundError("No images found in the specified folder.")

        # Summary Prompt
        summary_prompt_text = (
            "Provide a concise and detailed summary of the content in the image, including key objects, actions, and context."
        )

        # Process each image
        with open(summary_file_path, "a", encoding="utf-8") as summary_file:
            for image_path in image_files:
                print(f"Processing image: {image_path.name}")

                # Convert image to base64 data URL
                image_data_url = encode_image_to_base64(image_path)

                # Display the image for verification
                display_image(image_path)

                # Generate summary
                summary_result = image_summarize(summary_prompt_text, image_data_url)
                print(f"Summary for {image_path.name}:\n", summary_result)

                # Save summary to file
                summary_file.write(f"Image: {image_path.name}\n")
                summary_file.write(f"Summary: {summary_result}\n\n")
                print(f"Summary saved for {image_path.name}.")

        print(f"All summaries have been saved to {summary_file_path}.")

    except Exception as e:
        print(f"An error occurred: {e}")











# import os
# import base64
# from pathlib import Path
# import uuid
# import datetime

# from langchain_community.chat_models import ChatOpenAI
# #from langchain_openai import ChatOpenAI

# #
# #from langchain.chat_models import ChatOpenAI

# from langchain_core.messages import HumanMessage
# from PIL import Image

# # Set the API Key
# api_key = "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"  # Add your OpenAI API key here
# if not api_key:
#     raise ValueError("OPENAI_API_KEY not found. Please add it.")
# os.environ["OPENAI_API_KEY"] = api_key

# # Set project-specific environment variables
# uid = uuid.uuid4().hex[:6]
# current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# project_name = f"openai_image_summarization_{current_time}"
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = project_name


# def encode_image_to_base64(image_path):
#     """Encode image to base64 string."""
#     image_path = Path(image_path)
#     if not image_path.exists():
#         raise FileNotFoundError(f"Image not found at {image_path}")

#     with open(image_path, "rb") as image_file:
#         base64_image = base64.b64encode(image_file.read()).decode("utf-8")
#         return f"data:image/{image_path.suffix[1:]};base64,{base64_image}"


# def display_image(image_path):
#     """Display an image in the terminal using PIL."""
#     try:
#         img = Image.open(image_path)
#         # Uncomment below to show the image
#         # img.show()
#     except Exception as e:
#         print(f"Error displaying image: {e}")


# def image_summarize(prompt, image_data_url):
#     """Make image summary"""
#     chat = ChatOpenAI(model="gpt-4-turbo", max_tokens=1024)

#     # Create the message payload
#     msg = chat.invoke(
#         [
#             HumanMessage(
#                 content=[
#                     {"type": "text", "text": prompt},
#                     {
#                         "type": "image_url",  # API expects 'image_url'
#                         "image_url": {"url": image_data_url},
#                     },
#                 ]
#             )
#         ]
#     )
#     return msg.content


# if __name__ == "__main__":
#     # Input: Folder containing images
#     folder_path = "E:/Baarez/Automation/NBR_ChatBot/RAG_Chatbot - Copy/img2"  # Replace with your folder path
#     summary_file_path = "summary.txt"  # File to save summaries

#     try:
#         # List all image files in the folder
#         folder = Path(folder_path)
#         if not folder.exists():
#             raise FileNotFoundError(f"Folder not found: {folder_path}")

#         image_files = list(folder.glob("*.jpeg")) + list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
#         if not image_files:
#             raise FileNotFoundError("No images found in the specified folder.")

#         # Summary Prompt
#         summary_prompt_text = (
#             "Provide a concise and detailed summary of the content in the image, including key objects, actions, and context."
#         )

#         # Process each image
#         with open(summary_file_path, "a", encoding="utf-8") as summary_file:
#             for image_path in image_files:
#                 print(f"Processing image: {image_path.name}")

#                 # Convert image to base64 data URL
#                 image_data_url = encode_image_to_base64(image_path)

#                 # Display the image for verification
#                 display_image(image_path)

#                 # Generate summary
#                 summary_result = image_summarize(summary_prompt_text, image_data_url)
#                 print(f"Summary for {image_path.name}:\n", summary_result)

#                 # Save summary to file
#                 summary_file.write(f"Image: {image_path.name}\n")
#                 summary_file.write(f"Summary: {summary_result}\n\n")
#                 print(f"Summary saved for {image_path.name}.")

#         print(f"All summaries have been saved to {summary_file_path}.")

#     except Exception as e:
#         print(f"An error occurred: {e}")


