# LM Studio Advanced Features Reference

> Source: [lmstudio.ai/docs/advanced/tool-use](https://lmstudio.ai/docs/advanced/tool-use) | [lmstudio.ai/docs/developer](https://lmstudio.ai/docs/developer) | [github.com/lmstudio-ai/docs](https://github.com/lmstudio-ai/docs)

## Table of Contents

1. [Tool Use / Function Calling](#tool-use--function-calling)
2. [MCP (Model Context Protocol)](#mcp-model-context-protocol)
3. [Structured Output](#structured-output)
4. [Speculative Decoding](#speculative-decoding)
5. [Reasoning Models](#reasoning-models)
6. [Parallel Predictions](#parallel-predictions)
7. [Document RAG](#document-rag)
8. [Headless Deployment](#headless-deployment)
9. [Linux Systemd Service](#linux-systemd-service)
10. [Authentication & Security](#authentication--security)

---

## Tool Use / Function Calling

### Tool Definition Format

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {"type": "string", "description": "City name"}
      },
      "required": ["city"]
    }
  }
}
```

### Models with Native Tool Use Support

| Family | Examples |
|--------|----------|
| **Qwen** | Qwen2.5-7B-Instruct, Qwen3 series |
| **Llama** | Meta-Llama-3.1-8B-Instruct, Llama-3.2 |
| **Mistral** | Ministral-8B-Instruct |

Other models get default prompt-based tool support (less reliable).

### Workflow

```
1. Send user message + tool definitions
2. Model responds with tool_calls (or normal text)
3. Execute functions, add results as role:"tool" messages
4. Re-prompt model (optionally without tools) for final answer
```

### Python Example

```python
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
tools = [{"type": "function", "function": {"name": "get_weather", "description": "Get weather", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]

response = client.chat.completions.create(
    model="qwen/qwen3-8b",
    messages=[{"role": "user", "content": "Weather in Madrid?"}],
    tools=tools
)

if response.choices[0].message.tool_calls:
    tc = response.choices[0].message.tool_calls[0]
    result = get_weather(**json.loads(tc.function.arguments))
    # Feed result back and get final response
```

---

## MCP (Model Context Protocol)

LM Studio acts as MCP host. Config: `~/.lmstudio/mcp.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem-server", "/path/to/dir"]
    },
    "remote-tool": {
      "url": "https://mcp.example.com/search",
      "transport": "sse"
    }
  }
}
```

**Two modes:**
- **Configured** (in mcp.json): launched on startup, persistent
- **Ephemeral** (per-request via API `integrations` param): on-demand

---

## Structured Output

```bash
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [{"role": "user", "content": "Extract: John is 30"}],
    "response_format": {
      "type": "json_schema",
      "json_schema": {"name": "person", "schema": {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}, "required": ["name", "age"]}}
    }
  }'
```

Python: use Pydantic `BaseModel` as `response_format`. TypeScript: use Zod schemas.

---

## Speculative Decoding

Small draft model generates candidates; large model verifies in one pass.

```json
{"model": "qwen/qwen3-30b", "draft_model": "qwen/qwen3-4b", ...}
```

Requirements: same tokenizer/vocabulary. Best when draft accepts >70% tokens.

---

## Reasoning Models

DeepSeek R1 etc. return `reasoning_content` separately.

```json
{"reasoning": {"effort": "high"}}
```

---

## Parallel Predictions

```bash
lms load MODEL --parallel 4 --gpu max
```

Individual predictions slightly slower, but higher total throughput.

---

## Document RAG

Chat tab: attach `.pdf`, `.docx`, `.txt`. Auto-selects:
- **Full Context**: doc fits in context window → injected directly
- **RAG**: doc too large → chunked, embedded, semantic retrieval

---

## Headless Deployment

```bash
lms daemon up
lms load MODEL --gpu max -y
lms server start --port 1234
curl http://localhost:1234/v1/models
```

Or use `llmster` standalone: `curl -fsSL https://lmstudio.ai/install-llmster.sh | bash`

---

## Linux Systemd Service

```ini
[Unit]
Description=LM Studio Server
After=network.target

[Service]
Type=simple
ExecStartPre=/usr/local/bin/lms daemon up
ExecStartPre=/usr/local/bin/lms load MODEL --gpu max -y
ExecStart=/usr/local/bin/lms server start --port 1234
ExecStop=/usr/local/bin/lms server stop
ExecStopPost=/usr/local/bin/lms daemon down
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## Authentication & Security

1. Enable in Developer > Server Settings
2. Create token in app
3. Use: `Authorization: Bearer $LM_API_TOKEN`

Tokens support configurable permissions (read-only, inference, full access).
