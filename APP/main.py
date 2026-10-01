import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from routes import router


load_dotenv()


app = FastAPI(
    title="ComicCraft AI",
    description="AI Comic Generator using Gemini and Hugging Face",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# TEMPLATES
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

templates = Jinja2Templates(
    directory=os.path.join(
        BASE_DIR,
        "templates"
    )
)


app.state.templates = templates


# =========================================================
# ROUTES
# =========================================================

app.include_router(router)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "ComicCraft AI"
    }


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    import uvicorn

    host = os.getenv(
        "SERVER_HOST",
        "127.0.0.1"
    )

    port = int(
        os.getenv(
            "SERVER_PORT",
            "8000"
        )
    )

    uvicorn.run(
        "APP.main:app",
        host=host,
        port=port,
        reload=True
    )