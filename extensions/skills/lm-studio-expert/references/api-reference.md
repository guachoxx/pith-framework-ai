# LM Studio API — Complete Reference

> Source: [lmstudio.ai/docs/api](https://lmstudio.ai/docs/api) | [lmstudio.ai/docs/developer](https://lmstudio.ai/docs/developer) | [github.com/lmstudio-ai/docs](https://github.com/lmstudio-ai/docs)

## Table of Contents

1. [Server & Authentication](#server--authentication)
2. [OpenAI-Compatible Endpoints (/v1/)](#openai-compatible-endpoints)
3. [Native REST API (/api/v1/)](#native-rest-api)
4. [Anthropic-Compatible Endpoint](#anthropic-compatible-endpoint)
5. [Python SDK](#python-sdk)
6. [TypeScript SDK](#typescript-sdk)
7. [Common Parameters & Features](#common-parameters--features)

---

## Server & Authentication

**Default server:** `http://localhost:1234`

**Authentication (optional):**
```bash
export LM_API_TOKEN="your-token-here"
curl -H "Authorization: Bearer $LM_API_TOKEN" http://localhost:1234/v1/models
```

---

## OpenAI-Compatible Endpoints

### GET `/v1/models` — List loaded models

```bash
curl http://localhost:1234/v1/models
```

### POST `/v1/chat/completions` — Chat completions

```bash
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7,
    "max_tokens": 1024,
    "stream": false
  }'
```

**Parameters:** `model`, `messages`, `temperature`, `top_p`, `max_tokens`, `stream`, `tools`, `tool_choice`, `response_format`, `stop`

### POST `/v1/embeddings` — Text embeddings

```bash
curl -X POST http://localhost:1234/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "nomic-embed-text", "input": "Text to embed"}'
```

### POST `/v1/responses` — Stateful chat

```bash
curl -X POST http://localhost:1234/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_ID", "input": "Follow-up", "previous_response_id": "resp_abc123"}'
```

---

## Native REST API

### POST `/api/v1/chat` — Advanced chat (JIT, TTL, MCP)

```bash
curl -X POST http://localhost:1234/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_ID", "input": "Hello!", "context_length": 8192, "ttl": 3600}'
```

Extra params: `context_length`, `ttl`, `integrations` (MCP).

### POST `/api/v1/load` / `/api/v1/unload` — Model management

### POST `/api/v1/download` / GET `/api/v1/download-status` — Download models

---

## Anthropic-Compatible Endpoint

### POST `/v1/messages` — Claude-compatible

```bash
curl -X POST http://localhost:1234/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_ID", "messages": [{"role": "user", "content": "Hello!"}], "max_tokens": 1024}'
```

---

## Python SDK

```bash
pip install lmstudio
```

```python
import lmstudio as lms

# Simple
model = lms.llm()
response = model.respond("Hello!")

# Scoped
with lms.Client() as client:
    model = client.llm.model("qwen/qwen3-8b")
    response = model.respond("Hello!")

# Async
async with lms.AsyncClient() as client:
    model = client.llm.model("qwen/qwen3-8b")
    response = await model.respond("Hello!")

# Streaming
for chunk in model.respond_stream("Tell me a story"):
    print(chunk, end="", flush=True)

# Tool calling
def get_weather(city: str) -> str:
    return f"Sunny in {city}"
response = model.respond("Weather in Madrid?", tools=[get_weather])

# Structured output (Pydantic)
from pydantic import BaseModel
class Person(BaseModel):
    name: str
    age: int
result = model.respond("John is 30", response_format=Person)
```

---

## TypeScript SDK

```bash
npm install @lmstudio/sdk
```

```typescript
import { LMStudioClient } from "@lmstudio/sdk";
const client = new LMStudioClient();
const model = await client.llm.model("qwen/qwen3-8b");
const response = await model.respond("Hello!");
```

---

## Common Parameters & Features

| Feature | Endpoint | Parameter |
|---------|----------|-----------|
| Streaming | `/v1/chat/completions` | `stream: true` |
| Tool Calling | `/v1/chat/completions` | `tools` array |
| Structured Output | `/v1/chat/completions` | `response_format: {"type": "json_schema"}` |
| Speculative Decoding | `/v1/chat/completions` | `draft_model` |
| Auto-Eviction | `/api/v1/chat` | `ttl` (seconds) |
| Reasoning | `/v1/chat/completions` | `reasoning.effort` |
| Stateful Chat | `/v1/responses` | `previous_response_id` |
| MCP Integration | `/api/v1/chat` | `integrations` array |

### Model Lifecycle: NotDownloaded → OnDisk → InMemory → Active

### JIT Loading: API request for unloaded model auto-loads it (TTL=3600s default, auto-evict previous)
