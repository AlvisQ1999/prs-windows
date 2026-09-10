import base64
import io

import cv2
from PIL import Image
from matplotlib import pyplot as plt
from openai import OpenAI

from robot.object_detection import *


# ============================================================
# XCodeCLI API
# ============================================================

client = OpenAI(
    api_key="sk-",
    base_url="https://api2.xcodecli.com/v1"
)

MODEL = "gpt-5.5"


# ============================================================
# Grounding DINO
# ============================================================

grounding_dino = GroundingDino()


def object_detect_module(image, text="the human"):
    if text[-1] != ".":
        text = text + "."

    result = grounding_dino.predict(image, text)

    return result


# ============================================================
# Vision + Language Model
# ============================================================

def lmm_interaction(content, image):
    """
    GPT-5.5 multimodal request through XCodeCLI Responses API.
    """

    image = Image.fromarray(image)

    image_file = io.BytesIO()
    image.save(image_file, format="PNG")

    encoded_string = base64.b64encode(
        image_file.getvalue()
    ).decode("utf-8")

    image_url = f"data:image/png;base64,{encoded_string}"

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": content
                    },
                    {
                        "type": "input_image",
                        "image_url": image_url
                    }
                ]
            }
        ]
    )

    result = response.output_text

    if result is None:
        result = ""

    print("[LMM RESPONSE]:", repr(result))

    return result


# ============================================================
# Text-only LLM
# ============================================================

def llm_interaction(content="Hello World!", temperature=0.9):
    """
    GPT-5.5 text request through XCodeCLI Responses API.

    temperature is kept only to stay compatible with
    the original PRS function signature.
    """

    response = client.responses.create(
        model=MODEL,
        input=content
    )

    result = response.output_text

    if result is None:
        result = ""

    print("[LLM RESPONSE]:", repr(result))

    return result


# ============================================================
# Original Grounding DINO demo
# ============================================================

if __name__ == "__main__":
    im = cv2.imread("example.jpg")

    if im is None:
        print("example.jpg not found.")
    else:
        mat = object_detect_module(
            im,
            "the water bottle."
        )

        plt.imshow(mat)
        plt.show()