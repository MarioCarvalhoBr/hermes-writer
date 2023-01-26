import os
import requests
from io import BytesIO
import time

# Libs externs
import openai
from PIL import Image
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Load API_KEY from .env
API_KEY = os.getenv("API_KEY")

# Set API_KEY in openai
openai.api_key = API_KEY


PATH_FILE_CHAT_LOGS = "chat_logs.txt"
PATH_DIR_IMAGES = "images"

# Verify dir images
if not os.path.exists(PATH_DIR_IMAGES): # If not exists dir images
    os.makedirs(PATH_DIR_IMAGES) #  Create dir images

# Verify file chat_logs.txt
if not os.path.exists(PATH_FILE_CHAT_LOGS): # If not exists file chat_logs.txt
    with open(PATH_FILE_CHAT_LOGS, "w") as f: # Create file chat_logs.txt
        f.write("")
        f.close()

# Function to generate a response
def question(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0,
        max_tokens=700,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    text_result = response.choices[0].text
    text_result = text_result.replace("\n", "")
    return text_result

while True:
    '''
    Menu: 
    1 - Rewrite this text with others words:
    2 - Improve this text: 
    3 - Rewrite this text to the past tense: 
    4 - Enter a question: 
    5 - Exit 
    6 - Generate a new image:
    '''
    print("Menu Hermes 0.0.1")
    print("1 - Rewrite this text with others words: ")
    print("2 - Improve this text: ")
    print("3 - Rewrite this text to the past tense: ")
    print("4 - Enter a question: ")
    print("5 - Exit ")
    print("6 - Generate a new image:")

    # Input option
    option = input("Enter a option: ")

    text_option = ""
    if option == "6":
        text_option = "Generate a new image: "
        prompt = input(text_option)

        prompt = text_option + "\"" + prompt + "\""
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        path_name_image = PATH_DIR_IMAGES+"image_" + str(time.time()) + ".png"
        img.save(path_name_image)
        
        print('Image save local: ', path_name_image)
        print('Link web: ', image_url)
    else: 
        if option == "1":
            text_option = "Rewrite this text with others words: "
        elif option == "2":
            text_option = "Improve this text: "
        elif option == "3":
            text_option = "Rewrite this text to the past tense: "
        elif option == "4":
            print("Enter a question: ")
        elif option == "5":
            print("\nExiting Hermes... Bye bye.\n")
            break
        else:
            print("Enter a question: ")
        prompt = input(text_option)

        prompt = text_option + "\"" + prompt + "\""

        response = question(prompt)

        # Print size of response
        print("\nResponse:\n" + response)
        print("\nNumber of characters: " + str(len(response)))
        print("\n")

        # Add prompt and response in questions.txt
        with open(PATH_FILE_CHAT_LOGS, "a") as f:
            f.write("\n\nQuestion: " + prompt + "\nResponse: " + response + "")
