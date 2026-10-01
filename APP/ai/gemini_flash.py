import os
import base64
import requests

from io import BytesIO
from dotenv import load_dotenv

from google import genai
from google.genai import types
from huggingface_hub import InferenceClient


load_dotenv(override=True)


# ==============================
# GEMINI SETTINGS
# ==============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_TEXT_MODEL = os.getenv(
    "GEMINI_TEXT_MODEL",
    "gemini-3.8-flash"
)

GEMINI_IMAGE_MODEL = os.getenv(
    "GEMINI_IMAGE_MODEL",
    "gemini-3.8-flash-image"
)


# ==============================
# HUGGING FACE SETTINGS
# ==============================

HF_TOKEN = os.getenv("HF_TOKEN")

HF_TEXT_MODEL = os.getenv(
    "HF_TEXT_MODEL",
    "HuggingFaceH4/zephyr-7b-beta"
)

HF_IMAGE_MODEL = os.getenv(
    "HF_IMAGE_MODEL",
    "black-forest-labs/FLUX.1-schnell"
)


# ==============================
# POLLINATIONS SETTINGS
# ==============================

POLLINATIONS_API_KEY = os.getenv(
    "POLLINATIONS_API_KEY"
)

POLLINATIONS_IMAGE_MODEL = os.getenv(
    "POLLINATIONS_IMAGE_MODEL",
    "flux"
)


# ==============================
# GEMINI CLIENT
# ==============================

gemini_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ==============================
# HUGGING FACE CLIENT
# ==============================

hf_client = None

if HF_TOKEN:
    hf_client = InferenceClient(
        api_key=HF_TOKEN,
        provider="auto"
    )


# ==============================
# GEMINI TEXT GENERATION
# ==============================

def generate_gemini_text(prompt: str) -> str:

    if not gemini_client:
        raise RuntimeError(
            "GEMINI_API_KEY is missing in .env"
        )

    response = gemini_client.models.generate_content(
        model=GEMINI_TEXT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            max_output_tokens=2048
        )
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text


# ==============================
# GEMINI IMAGE GENERATION
# ==============================

def generate_gemini_image(prompt: str) -> bytes:

    if not gemini_client:
        raise RuntimeError(
            "GEMINI_API_KEY is missing in .env"
        )

    response = gemini_client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        )
    )

    for candidate in response.candidates or []:

        if not candidate.content:
            continue

        for part in candidate.content.parts or []:

            if part.inline_data and part.inline_data.data:

                image_data = part.inline_data.data

                if isinstance(image_data, str):
                    return base64.b64decode(
                        image_data
                    )

                return image_data

    raise RuntimeError(
        "Gemini did not return an image."
    )


# ==============================
# HUGGING FACE TEXT GENERATION
# ==============================

def generate_huggingface_text(prompt: str) -> str:

    if not hf_client:
        raise RuntimeError(
            "HF_TOKEN is missing in .env"
        )

    result = hf_client.chat.completions.create(
        model=HF_TEXT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2048,
        temperature=0.8
    )

    return result.choices[0].message.content


# ==============================
# HUGGING FACE IMAGE GENERATION
# ==============================

def generate_huggingface_image(prompt: str) -> bytes:

    if not hf_client:
        raise RuntimeError(
            "HF_TOKEN is missing in .env"
        )

    image = hf_client.text_to_image(
        prompt=prompt,
        model=HF_IMAGE_MODEL
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


# ==============================
# POLLINATIONS IMAGE GENERATION
# ==============================

def generate_pollinations_image(prompt: str) -> bytes:

    if not POLLINATIONS_API_KEY:
        raise RuntimeError(
            "POLLINATIONS_API_KEY is missing in .env"
        )

    from urllib.parse import quote

    encoded_prompt = quote(
        prompt,
        safe=""
    )

    url = (
        "https://gen.pollinations.ai/image/"
        + encoded_prompt
    )

    headers = {
        "Authorization": (
            f"Bearer {POLLINATIONS_API_KEY}"
        )
    }

    params = {
        "model": POLLINATIONS_IMAGE_MODEL,
        "width": 1024,
        "height": 1024,
        "nologo": "true"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=120
    )

    if response.status_code != 200:

        raise RuntimeError(
            "Pollinations image generation failed: "
            f"{response.status_code} - "
            f"{response.text}"
        )

    if not response.content:

        raise RuntimeError(
            "Pollinations returned an empty image."
        )

    return response.content


# ==============================
# GENERATE 5 POLLINATIONS IMAGES
# ==============================

def generate_pollinations_images(
    prompt: str,
    count: int = 5
) -> list[bytes]:

    images = []

    for i in range(count):

        panel_prompt = (
            f"{prompt}\n"
            f"Comic panel {i + 1} of {count}. "
            f"Keep the same character and "
            f"visual style across all panels."
        )

        image = generate_pollinations_image(
            panel_prompt
        )

        images.append(image)

    return images