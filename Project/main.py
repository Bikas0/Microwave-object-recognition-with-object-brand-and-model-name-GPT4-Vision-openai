import os
import base64
import requests
import string
import re
from dotenv import load_dotenv
from object_detection import object


# OpenAI API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def extract_first_sentence(text):
    # Using regular expression to find the first sentence
    match = re.match(r'(.*?[.!?])', text)
    if match:
        return match.group(1)
    else:
        return "No sentence found"


def word_lengths(input_string):
    words = input_string.split()
    return [len(word) for word in words]


def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def perform_image_processing(image_path):
    # Getting the base64 string
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
                        "text": "What’s the brand name in this image? What's the model name in this image?"
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
        "max_tokens": 60
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    # Extracting brand name and model name
    message_content = response_data['choices'][0]['message']['content']

    brand_name_start = message_content.find('"') + 1
    brand_name_end = message_content.find('"', brand_name_start)
    brand_name = message_content[brand_name_start:brand_name_end]
    if len(word_lengths(brand_name)) >= 4:
        brand_name = extract_first_sentence(brand_name)

    brands_name_start = message_content.find('"', brand_name_end + 1) + 1
    brands_name_end = message_content.find('"', brands_name_start)
    brands_name = remove_punctuation(message_content[brands_name_start:brands_name_end])
    if len(word_lengths(brands_name)) >= 3:
        brands_name = ""
    # Printing the extracted brand name and model name
    brand_name = str(remove_punctuation(brand_name)) + " " + str(brands_name)
    # print("Brand Name: ", brand_name)

    pattern = re.compile(r'\bsorry\b', re.IGNORECASE)
    # Use findall to get all matches
    matches = pattern.findall(brand_name.lower())
    model_name, _ = os.path.splitext(os.path.basename(image_path))

    if matches == "sorry":
        brand_name = None
        return brand_name, model_name

    else:
        return brand_name, model_name


def process_image(img_path):
    image_path = object(img_path)

    if image_path is not None:
        image_path = os.path.join("image", image_path)
    else:
        image_path = img_path

    band_name, model_name = perform_image_processing(image_path)
    return band_name, model_name, image_path
