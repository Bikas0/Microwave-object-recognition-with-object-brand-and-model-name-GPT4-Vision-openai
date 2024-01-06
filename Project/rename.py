# import base64
# import requests
# from dotenv import load_dotenv
# import os
#
# # Function to encode the image
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')
#
#
# # Function to get brand name and model name from OpenAI API
# def get_brand_and_model(image_path):
#     base64_image = encode_image(image_path)
#
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     }
#
#     payload = {
#         "model": "gpt-4-vision-preview",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": "What’s the brand name and model name in this image?"
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}"
#                         }
#                     }
#                 ]
#             }
#         ],
#         "max_tokens": 300
#     }
#
#     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#     response_data = response.json()
#
#     # Check if 'choices' key is present in the response
#     if 'choices' in response_data:
#         # Extracting brand name
#         message_content = response_data['choices'][0]['message']['content']
#
#         brand_name_start = message_content.find('"') + 1
#         brand_name_end = message_content.find('"', brand_name_start)
#         brand_name = message_content[brand_name_start:brand_name_end]
#
#
#         model_name_start = message_content.find('"', brand_name_end + 1) + 1
#         model_name_end = message_content.find('"', model_name_start)
#         model_name = message_content[model_name_start:model_name_end]
#
#
#         return brand_name, model_name
#     else:
#         print("Error: Unexpected response structure from OpenAI API.")
#         return None
#
#
# # Load OpenAI API key from environment variable
# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
#
# # Path to the folder containing the images
# folder_path = "image"
#
# # Loop through all files in the folder
# for filename in os.listdir(folder_path):
#     # Check if the file is an image file
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
#         # Construct the full path
#         image_path = os.path.join(folder_path, filename)
#
#         # Get brand name using OpenAI API
#         brand_name, model_name = get_brand_and_model(image_path)
#
#         print(f"File: {filename}--->{brand_name}---{model_name}")



import base64
import requests
from dotenv import load_dotenv
import os

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to get brand name and model name from OpenAI API
def get_brand_and_model(image_path):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s the brand name and model name in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    # Check if 'choices' key is present in the response
    if 'choices' in response_data:
        # Extracting brand name
        message_content = response_data['choices'][0]['message']['content']

        brand_name_start = message_content.find('"') + 1
        brand_name_end = message_content.find('"', brand_name_start)
        brand_name = message_content[brand_name_start:brand_name_end]

        model_name_start = message_content.find('"', brand_name_end + 1) + 1
        model_name_end = message_content.find('"', model_name_start)
        model_name = message_content[model_name_start:model_name_end]

        return brand_name, model_name
    else:
        print("Error: Unexpected response structure from OpenAI API.")
        return None, None  # Return None for both brand_name and model_name

# Load OpenAI API key from environment variable
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Path to the folder containing the images
folder_path = "image"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image file
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
        # Construct the full path
        image_path = os.path.join(folder_path, filename)

        # Get brand name using OpenAI API
        brand_name, model_name = get_brand_and_model(image_path)

        if brand_name is not None and model_name is not None:
            print(f"File: {filename} ---> {brand_name} --- {model_name}")
        else:
            print(f"Error processing file: {filename}")
