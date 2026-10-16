import hmac
import logging
import os
import threading

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pysentimiento import create_analyzer

logger = logging.getLogger("uvicorn.error")

# Shared secret with the API (header X-IA-Key). Empty = open, dev only:
# the production image sets IA_REQUIRE_KEY=1 and refuses to boot without it.
API_KEY = os.environ.get("IA_API_KEY", "")
REQUIRE_KEY = os.environ.get("IA_REQUIRE_KEY") == "1"
# Inferences running at once; the rest get an immediate 503 (the API treats
# 5xx as "IA unavailable" and retries later, it never loses the analysis).
MAX_CONCURRENCY = int(os.environ.get("IA_MAX_CONCURRENCY", "2"))
# The API trims messages to this length before sending them.
MAX_TEXT_LENGTH = int(os.environ.get("IA_MAX_TEXT_LENGTH", "2000"))
MAX_BODY_BYTES = int(os.environ.get("IA_MAX_BODY_BYTES", "16384"))

if REQUIRE_KEY and len(API_KEY) < 32:
    raise RuntimeError("IA_API_KEY is missing or shorter than 32 chars (IA_REQUIRE_KEY=1)")
if not API_KEY:
    logger.warning("IA_API_KEY is not set: /analyze_message accepts unauthenticated requests")

# Interactive docs only where the service is open (dev).
docs = {} if not REQUIRE_KEY else {"docs_url": None, "redoc_url": None, "openapi_url": None}
app = FastAPI(title="Analyzer Sentiment API", version="1.0.0", **docs)
analyzer = create_analyzer(task="sentiment", lang="es")
slots = threading.BoundedSemaphore(MAX_CONCURRENCY)


class TextInput(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_TEXT_LENGTH)


@app.middleware("http")
async def limit_body(request: Request, call_next):
    if request.method == "POST":
        length = request.headers.get("content-length")
        if length is None or not length.isdigit():
            return JSONResponse({"detail": "Content-Length required"}, status_code=411)
        if int(length) > MAX_BODY_BYTES:
            return JSONResponse({"detail": "Payload too large"}, status_code=413)
    return await call_next(request)


def require_key(x_ia_key: str = Header(default="")):
    if API_KEY and not hmac.compare_digest(x_ia_key.encode(), API_KEY.encode()):
        raise HTTPException(status_code=401, detail="Invalid IA key")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    # The model loads at import time, so answering means it is ready.
    return {"status": "ok"}


@app.post("/analyze_message", dependencies=[Depends(require_key)])
def analyze_message(input: TextInput):
    if not slots.acquire(blocking=False):
        raise HTTPException(status_code=503, detail="Busy", headers={"Retry-After": "5"})
    try:
        result = analyzer.predict(input.text)
        return {
            "text": input.text,
            "label": result.output,
            "probabilities": result.probas
        }
    except Exception:
        logger.exception("analysis failed")
        raise HTTPException(status_code=500, detail="Analysis failed")
    finally:
        slots.release()
