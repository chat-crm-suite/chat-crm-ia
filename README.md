<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/chat-crm-suite/.github/main/brand/svg/chatcrm-lockup-dark.svg">
  <img alt="ChatCRM" src="https://raw.githubusercontent.com/chat-crm-suite/.github/main/brand/svg/chatcrm-lockup-light.svg" width="340">
</picture>

### ChatCRM AI

Sentiment analysis for customer messages.

[![License: PolyForm Noncommercial](https://img.shields.io/badge/license-PolyForm%20NC%201.0-006239)](LICENSE)
![Python 3.12](https://img.shields.io/badge/Python-3.12-006239?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.119-006239?logo=fastapi&logoColor=white)

**English** · [Español](README.es.md)

</div>

---

## Overview

`chat-crm-ia` is the optional AI service of ChatCRM. The [API](https://github.com/chat-crm-suite/chat-crm-api)
sends it customer messages and gets back their sentiment, which feeds the conversation view and the metrics
dashboard. It uses [pysentimiento](https://github.com/pysentimiento/pysentimiento), a transformer model trained
for **Spanish**. ChatCRM works without it; only the sentiment features need it. See the
[organization overview](https://github.com/chat-crm-suite).

## API

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Liveness check |
| `POST` | `/analyze_message` | Sentiment of one message |

```bash
curl -s -X POST http://localhost:8000/analyze_message \
  -H 'Content-Type: application/json' \
  -d '{"text": "Gracias, el pedido llegó perfecto"}'
```

```json
{
  "text": "Gracias, el pedido llegó perfecto",
  "label": "POS",
  "probabilities": { "POS": 0.98, "NEU": 0.01, "NEG": 0.01 }
}
```

`label` is `POS`, `NEU` or `NEG`. Interactive docs: `http://localhost:8000/docs`.

## Quick start

### Docker

```bash
docker build -t chat-crm-ia .
docker run --rm -p 8000:8000 chat-crm-ia
```

With the full ChatCRM stack, start it with the `ia` profile from the parent folder:
`docker compose --profile ia up --build -d`. The API reaches it through `IA_URL`.

### Without Docker

Requires Python 3.12.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
hypercorn main:app --bind 0.0.0.0:8000 --reload
```

The first start downloads the model from Hugging Face (several hundred MB), so it takes a while.

## Tech stack

Python 3.12 · FastAPI · Hypercorn · pysentimiento · Transformers · PyTorch.

## Contributing

Read the [contributing guide](https://github.com/chat-crm-suite/.github/blob/main/CONTRIBUTING.md). Report
vulnerabilities privately as described in the [security policy](https://github.com/chat-crm-suite/.github/blob/main/SECURITY.md).

## License

Licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE):

- **Noncommercial use** is free: use, modify and distribute the code while keeping the copyright notices ([`NOTICE`](NOTICE)).
- **Commercial use** requires a commercial license. Organizations below USD 100,000/year in revenue get it for free;
  above that, an annual fee or revenue share — see [`COMMERCIAL.md`](COMMERCIAL.md).
- **Authorship**: `Copyright (c) 2026 Jerremi Aron Chancan Labajos`. Commercial use requires the visible credit
  "Built on chat-crm".

The pysentimiento models have their own licenses; check them before commercial use.

Commercial licensing: **chancanjeremiaron@gmail.com**
