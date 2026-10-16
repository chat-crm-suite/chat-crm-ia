FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/hf

WORKDIR /app

# uid 1000 = host user in WSL (dev bind mounts) and the non-root prod user.
RUN useradd --uid 1000 --create-home appuser

COPY requirements.txt .

# CPU-only torch: the servers have no GPU, and the default CUDA wheels add
# several GB. Installed first so requirements.txt finds torch==2.9.0 satisfied.
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch==2.9.0 \
    && pip install -r requirements.txt

# Bake the model into the image: no download at boot, no outbound network in prod.
RUN python -c "from pysentimiento import create_analyzer; create_analyzer(task='sentiment', lang='es')" \
    && chown -R appuser:appuser /opt/hf

EXPOSE 8000

FROM base AS dev
COPY . .
USER appuser
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000", "--reload"]

FROM base AS production
ENV HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    IA_REQUIRE_KEY=1
COPY main.py .
USER appuser
# One worker: each worker loads its own copy of the model into RAM.
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)"
