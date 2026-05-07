# LM Studio CLI (`lms`) — Complete Reference

> Source: [lmstudio.ai/docs/cli](https://lmstudio.ai/docs/cli) | [github.com/lmstudio-ai/docs](https://github.com/lmstudio-ai/docs)
> CLI Version: 0.0.47+

## Table of Contents

1. [Installation & Prerequisites](#installation--prerequisites)
2. [Local Models Commands](#local-models-commands)
3. [Server Commands](#server-commands)
4. [Log Streaming](#log-streaming)
5. [Daemon (Headless) Commands](#daemon-headless-commands)
6. [LM Link Commands](#lm-link-commands)
7. [Runtime Commands](#runtime-commands)
8. [Develop & Publish (Beta)](#develop--publish-beta)
9. [Model Storage Structure](#model-storage-structure)

---

## Installation & Prerequisites

- `lms` ships with LM Studio — no separate install needed.
- Binary added to system PATH automatically on first LM Studio launch.
- The desktop app must run at least once to initialize CLI.
- Verify: `lms --help`
- Windows path: `%USERPROFILE%\.lmstudio\bin\lms.exe`
- macOS/Linux path: `~/.lmstudio/bin/lms`

---

## Local Models Commands

### `lms chat [model-key]`

Interactive terminal chat session with a model.

```bash
lms chat                          # chat with currently loaded model
lms chat qwen/qwen3-8b           # load and chat with specific model
```

- Press `Ctrl+C` to interrupt generation.
- If model isn't loaded, it auto-loads it.

### `lms get [keyword|URL]`

Search and download models from Hugging Face.

```bash
lms get deepseek-r1               # interactive search by keyword
lms get https://huggingface.co/publisher/model  # direct URL download
lms get qwen3 --mlx               # filter MLX-only models (Apple Silicon)
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--mlx` | Filter for MLX format models only |

### `lms load <model-key> [options]`

Load a model into memory with fine-grained configuration.

```bash
lms load qwen/qwen3-4b
lms load qwen/qwen3-4b --gpu max --context-length 8192
lms load qwen/qwen3-4b --gpu 0.7 --ttl 3600 --identifier my-model
lms load qwen/qwen3-4b --estimate-only
lms load qwen/qwen3-4b --parallel 4 --yes
```

**Flags:**
| Flag | Values | Description |
|------|--------|-------------|
| `--gpu <ratio>` | `off`, `max`, `auto`, `0.0`-`1.0` | GPU offload ratio. Default: auto |
| `-c, --context-length <N>` | integer | Token context window size |
| `--parallel <count>` | integer | Max concurrent predictions (continuous batching) |
| `--ttl <seconds>` | integer | Auto-unload after N seconds idle. No default for manual loads |
| `--identifier <name>` | string | Custom identifier for API reference |
| `--estimate-only` | flag | Print VRAM/RAM estimate without loading |
| `-y, --yes` | flag | Skip confirmation prompts (scripting) |

**Key behaviors:**
- Without `--ttl`, manually loaded models stay indefinitely.
- JIT-loaded models (via API) default to TTL=3600s.
- `--estimate-only` is critical for capacity planning before loading.

### `lms unload [identifier]`

Remove model(s) from memory.

```bash
lms unload                        # interactive selection
lms unload my-model               # unload by identifier
lms unload --all                  # unload ALL loaded models
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--all` | Unload all currently loaded models |

### `lms ls [modelKey] [options]`

List models available on disk.

```bash
lms ls                            # list all models
lms ls --variants                 # show all quantization variants
lms ls --llm                      # only LLM models
lms ls --embedding                # only embedding models
lms ls --json                     # machine-readable output
lms ls qwen/qwen3-8b             # show variants for specific model
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--variants` | Show all quantization variants per model |
| `--llm` | Filter LLM models only |
| `--embedding` | Filter embedding models only |
| `--json` | JSON output to stdout |

### `lms ps [options]`

List models currently loaded in memory.

```bash
lms ps                            # human-readable table
lms ps --json                     # JSON with status, queued requests, memory
```

### `lms import <file-path>`

Import an external model file (.gguf) into LM Studio.

```bash
lms import ~/Downloads/my-model.gguf
```

- Interactive prompts guide publisher/model name placement.
- Places file into `~/.lmstudio/models/<publisher>/<model>/` structure.

---

## Server Commands

### `lms server start [options]`

Start the local API server.

```bash
lms server start                  # default port 1234
lms server start --port 8080      # custom port
```

Exposes: `/v1/*` (OpenAI), `/api/v0/*` (native), `/api/v1/*` (advanced + MCP).

### `lms server stop`

Graceful shutdown: SIGTERM → drain → complete in-flight → unload → cleanup.

### `lms server status`

Returns: ON/OFF, port number, loaded models.

---

## Log Streaming

### `lms log stream [options]`

Real-time log output for debugging and monitoring.

```bash
lms log stream                                    # default: model source
lms log stream --source server                    # HTTP request logs
lms log stream --source model --filter input      # model input only
lms log stream --source model --filter output --stats  # output + perf metrics
lms log stream --json                             # machine-readable JSON
```

**Flags:**
| Flag | Values | Description |
|------|--------|-------------|
| `-s, --source` | `model` (default), `server` | Log origin |
| `--filter` | `input`, `output`, `both` | Restrict model logs |
| `--stats` | flag | Include tokens/sec metrics |
| `--json` | flag | Newline-separated JSON format |

---

## Daemon (Headless) Commands

| Command | Description |
|---------|-------------|
| `lms daemon up` | Start headless daemon (no GUI) |
| `lms daemon down` | Stop daemon |
| `lms daemon status` | Check daemon state |
| `lms daemon update` | Update inference runtime |

---

## LM Link Commands

| Command | Description |
|---------|-------------|
| `lms link enable` | Enable LM Link |
| `lms link disable` | Disable LM Link |
| `lms link status` | Check connection status |
| `lms link set-device-name <name>` | Set device name |
| `lms link set-preferred-device <device>` | Set preferred device |

---

## Runtime Commands

| Command | Description |
|---------|-------------|
| `lms runtime update` | Install/update runtimes (llama.cpp, MLX) |
| `lms runtime list` | Show available runtimes |

**Runtimes:** llama.cpp (all platforms, GGUF), Apple MLX (M-series only).

---

## Develop & Publish (Beta)

| Command | Description |
|---------|-------------|
| `lms clone <artifact>` | Clone from Hub (metadata only) |
| `lms push` | Upload to Hub (from dir with model.yaml) |
| `lms dev` | Plugin dev server |
| `lms login` | Authenticate with Hub |
| `lms logout` | Log out |
| `lms whoami` | Check auth status |

---

## Model Storage Structure

```
~/.lmstudio/
├── bin/                  # lms CLI binary
├── models/               # Downloaded models (publisher/model/file.gguf)
├── config-presets/       # Inference presets
├── conversations/        # Chat history (JSON)
├── server-logs/          # Server log files
├── mcp.json              # MCP server configuration
├── settings.json         # Application settings
├── projects/             # User projects
└── extensions/           # Installed extensions
```
