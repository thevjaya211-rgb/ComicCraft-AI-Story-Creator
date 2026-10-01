from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import base64

from ai.gemini_flash import (
    generate_gemini_text,
    generate_gemini_image,
    generate_huggingface_text,
    generate_huggingface_image,
    generate_pollinations_images,
)


router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str
    provider: str = "gemini"
    type: str = "text"


# =========================================================
# HOME PAGE
# =========================================================

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# =========================================================
# TEXT GENERATION
# =========================================================

@router.post("/generate")
async def generate(request: PromptRequest):

    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty."
        )

    try:

        provider = request.provider.lower()

        # ---------------- GEMINI ----------------
        if provider == "gemini":

            result = generate_gemini_text(
                request.prompt
            )

        # ---------------- HUGGING FACE ----------------
        elif provider in ["huggingface", "hf"]:

            result = generate_huggingface_text(
                request.prompt
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Invalid provider."
            )

        return {
            "success": True,
            "result": result
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================================================
# IMAGE GENERATION - 5 COMIC PANELS
# =========================================================

@router.post("/generate-image")
async def generate_image(request: PromptRequest):

    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Image prompt cannot be empty."
        )

    try:

        provider = request.provider.lower()

        images = []

        # =================================================
        # POLLINATIONS - GENERATE 5 IMAGES
        # =================================================

        if provider == "pollinations":

            image_list = generate_pollinations_images(
                request.prompt,
                count=5
            )

            for image_bytes in image_list:

                image_base64 = base64.b64encode(
                    image_bytes
                ).decode("utf-8")

                images.append(
                    f"data:image/png;base64,{image_base64}"
                )

        # =================================================
        # GEMINI - GENERATE 5 IMAGES
        # =================================================

        elif provider == "gemini":

            for i in range(5):

                panel_prompt = (
                    f"{request.prompt}\n"
                    f"Comic panel {i + 1} of 5. "
                    f"Keep the same character and "
                    f"visual style across all panels."
                )

                image_bytes = generate_gemini_image(
                    panel_prompt
                )

                image_base64 = base64.b64encode(
                    image_bytes
                ).decode("utf-8")

                images.append(
                    f"data:image/png;base64,{image_base64}"
                )

        # =================================================
        # HUGGING FACE - GENERATE 5 IMAGES
        # =================================================

        elif provider in ["huggingface", "hf"]:

            for i in range(5):

                panel_prompt = (
                    f"{request.prompt}\n"
                    f"Comic panel {i + 1} of 5. "
                    f"Keep the same character and "
                    f"visual style across all panels."
                )

                image_bytes = generate_huggingface_image(
                    panel_prompt
                )

                image_base64 = base64.b64encode(
                    image_bytes
                ).decode("utf-8")

                images.append(
                    f"data:image/png;base64,{image_base64}"
                )

        else:

            raise HTTPException(
                status_code=400,
                detail="Invalid provider."
            )

        return {
            "success": True,
            "images": images,
            "count": len(images)
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )