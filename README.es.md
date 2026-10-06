<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/chat-crm-suite/.github/main/brand/svg/chatcrm-lockup-dark.svg">
  <img alt="ChatCRM" src="https://raw.githubusercontent.com/chat-crm-suite/.github/main/brand/svg/chatcrm-lockup-light.svg" width="340">
</picture>

### ChatCRM · IA

Análisis de sentimiento de los mensajes de clientes.

[![Licencia: PolyForm Noncommercial](https://img.shields.io/badge/licencia-PolyForm%20NC%201.0-006239)](LICENSE)
![Python 3.12](https://img.shields.io/badge/Python-3.12-006239?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.119-006239?logo=fastapi&logoColor=white)

[English](README.md) · **Español**

</div>

---

## Resumen

`chat-crm-ia` es el servicio de IA opcional de ChatCRM. La [API](https://github.com/chat-crm-suite/chat-crm-api)
le envía los mensajes de los clientes y recibe su sentimiento, que alimenta la vista de conversaciones y el panel
de métricas. Usa [pysentimiento](https://github.com/pysentimiento/pysentimiento), un modelo transformer entrenado
para **español**. ChatCRM funciona sin este servicio; solo lo necesitan las funciones de sentimiento. Ver el
[resumen de la organización](https://github.com/chat-crm-suite).

## API

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/` | Comprobación de que el servicio responde |
| `POST` | `/analyze_message` | Sentimiento de un mensaje |

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

`label` es `POS`, `NEU` o `NEG`. Documentación interactiva: `http://localhost:8000/docs`.

## Inicio rápido

### Docker

```bash
docker build -t chat-crm-ia .
docker run --rm -p 8000:8000 chat-crm-ia
```

Con el stack completo de ChatCRM, levántalo con el perfil `ia` desde la carpeta padre:
`docker compose --profile ia up --build -d`. La API lo encuentra mediante `IA_URL`.

### Sin Docker

Requiere Python 3.12.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
hypercorn main:app --bind 0.0.0.0:8000 --reload
```

El primer arranque descarga el modelo desde Hugging Face (varios cientos de MB), así que tarda un poco.

## Stack

Python 3.12 · FastAPI · Hypercorn · pysentimiento · Transformers · PyTorch.

## Contribuir

Lee la [guía de contribución](https://github.com/chat-crm-suite/.github/blob/main/CONTRIBUTING.md#contribuir-a-chatcrm).
Reporta las vulnerabilidades en privado, como indica la
[política de seguridad](https://github.com/chat-crm-suite/.github/blob/main/SECURITY.md#política-de-seguridad).

## Licencia

Bajo la [PolyForm Noncommercial License 1.0.0](LICENSE):

- **El uso no comercial** es gratuito: usa, modifica y distribuye el código conservando los avisos de copyright ([`NOTICE`](NOTICE)).
- **El uso comercial** requiere una licencia comercial. Las organizaciones con ingresos menores a USD 100.000 al año
  la obtienen gratis; por encima, una cuota anual o un porcentaje de ingresos: ver [`COMMERCIAL.md`](COMMERCIAL.md).
- **Autoría**: `Copyright (c) 2026 Jerremi Aron Chancan Labajos`. El uso comercial exige el crédito visible
  "Built on chat-crm".

Los modelos de pysentimiento tienen sus propias licencias; revísalas antes de un uso comercial.

Licencias comerciales: **chancanjeremiaron@gmail.com**
