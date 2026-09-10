# import openai
import os
from matplotlib import pyplot as plt
from openai import OpenAI
# from zhipuai import ZhipuAI
import cv2
import base64
import io
from PIL import Image, ImageDraw
from robot.object_detection import *


client = OpenAI(
    api_key="sk-BlYDwFLm7krPAwTKflqXt01q8nEIwhZB6s41EIjKGIe16ugN",
    base_url="https://api2.xcodecli.com/v1"
)
grounding_dino = GroundingDino()


def object_detect_module(image, text='the human'):
    if text[-1] != '.':
        text = text + '.'
    result = grounding_dino.predict(image, text)
    return result


def lmm_interaction(content, image):
    image = Image.fromarray(image)
    image_file = io.BytesIO()
    image.save(image_file, format='PNG')
    encoded_string = base64.b64encode(image_file.getvalue()).decode()
    response = client.chat.completions.create(
        model="gpt-5.5",  # Fill in the name of the model that needs to be called
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/png;base64,{encoded_string}"
                      }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    res = response.choices[0].message.content
    return res


def llm_interaction(content='Hello World!', temperature=0.9):
    response = client.chat.completions.create(
        model="gpt-5.5",  #   gpt-3.5-turbo-0125
        messages=[
            {"role": "user", "content": content}
        ],
    )
    res = response.choices[0].message.content
    return res

if __name__ == '__main__':
    image_path = os.path.join(os.path.dirname(__file__), 'example.jpg')
    im = cv2.imread(image_path)
    if im is None:
        raise FileNotFoundError('Could not read image: {}'.format(image_path))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    mat = object_detect_module(im, 'the water bottle.')
    if mat is None:
        print('No water bottle detected')
    else:
        print('Water bottle detected; mask shape:', mat.shape)
        plt.imshow(mat)
        plt.axis('off')
        plt.show()
