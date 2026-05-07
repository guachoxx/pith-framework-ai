# LM Studio Diagnostics & Troubleshooting Reference

> Source: [lmstudio.ai/docs](https://lmstudio.ai/docs) | [github.com/lmstudio-ai/docs](https://github.com/lmstudio-ai/docs)

## Table of Contents

1. [Quick Health Check Protocol](#quick-health-check-protocol)
2. [Diagnostic Commands Cheat Sheet](#diagnostic-commands-cheat-sheet)
3. [Common Issues & Fixes](#common-issues--fixes)
4. [Performance Diagnostics](#performance-diagnostics)
5. [Memory & GPU Diagnostics](#memory--gpu-diagnostics)
6. [Server & Network Diagnostics](#server--network-diagnostics)
7. [Log Analysis Patterns](#log-analysis-patterns)
8. [System Requirements](#system-requirements)

---

## Quick Health Check Protocol

Run this sequence to assess health in under 60 seconds:

```bash
lms status                        # 1. Is LM Studio running?
lms server status                 # 2. Is the server up?
lms ps --json                     # 3. What models are loaded?
lms ls --json                     # 4. What's available on disk?
curl -s http://localhost:1234/v1/models | head -20  # 5. Can API respond?
# 6. Quick inference test:
curl -s -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_ID", "messages": [{"role": "user", "content": "Say hello"}], "max_tokens": 10}'
```

---

## Diagnostic Commands Cheat Sheet

### Status & State

| Command | What it reveals |
|---------|----------------|
| `lms status` | App state, loaded models, server port |
| `lms server status` | Server ON/OFF, port |
| `lms ps` | Loaded models, memory |
| `lms ps --json` | Detailed: model IDs, status, queued requests |
| `lms ls --variants` | All quantization variants per model |

### Real-Time Monitoring

| Command | What it reveals |
|---------|----------------|
| `lms log stream` | Live model I/O |
| `lms log stream --source server` | HTTP requests, errors |
| `lms log stream --source model --stats` | Token speed (tok/s) |
| `lms log stream --json` | Machine-parseable stream |

### Resource Estimation

| Command | What it reveals |
|---------|----------------|
| `lms load MODEL --estimate-only` | VRAM/RAM needed |
| `lms load MODEL --estimate-only --context-length 32768` | Large context estimate |
| `lms load MODEL --estimate-only --gpu max` | Full GPU offload estimate |

---

## Common Issues & Fixes

### "lms: command not found"

LM Studio must be launched at least once. Manual fix:
```bash
# Windows
set PATH=%PATH%;%USERPROFILE%\.lmstudio\bin
# macOS/Linux
export PATH="$PATH:$HOME/.lmstudio/bin"
```

### Server not starting / port in use

```bash
# Windows: check port
netstat -ano | findstr :1234
# Linux/macOS
lsof -i :1234
# Fix: use different port
lms server start --port 8080
```

### Model fails to load (out of memory)

```bash
lms load MODEL --estimate-only           # Step 1: check requirements
lms load MODEL --gpu 0.5                 # Step 2: reduce GPU
lms load MODEL --context-length 4096 --gpu 0.5  # Step 3: reduce context
lms load MODEL --gpu off                 # Step 4: CPU-only
```

### Slow inference

```bash
lms log stream --source model --filter output --stats   # Monitor tok/s
# Causes: low GPU offload, large context, model too big for VRAM
```

### API 401 Unauthorized

```bash
export LM_API_TOKEN="your-token"
curl -H "Authorization: Bearer $LM_API_TOKEN" http://localhost:1234/v1/models
```

### API 404 / model not found

```bash
lms ps --json                # Verify loaded model identifier
curl http://localhost:1234/v1/models   # Check available via API
```

### Malformed tool calls

Use models with native tool support: Qwen, Llama 3.1+, Mistral.

---

## Performance Diagnostics

### Measure Token Speed

```bash
# Terminal 1: Monitor
lms log stream --source model --filter output --stats

# Terminal 2: Test prompt
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_ID", "messages": [{"role": "user", "content": "Write 500 words about AI"}], "max_tokens": 500}'
```

### Compare Quantizations

```bash
lms load publisher/model@q4_k_m --gpu max -y  # test, note tok/s
lms unload --all
lms load publisher/model@q8_0 --gpu max -y    # test, note tok/s
```

### Benchmark Parallel Predictions

```bash
lms load MODEL --parallel 4 --gpu max
# Send 4 concurrent requests
seq 4 | xargs -P4 -I{} curl -s -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_ID", "messages": [{"role": "user", "content": "Hello {}"}], "max_tokens": 50}'
```

---

## Memory & GPU Diagnostics

### Estimate Before Loading

```bash
for ctx in 2048 4096 8192 16384 32768; do
  echo "=== Context: $ctx ==="
  lms load MODEL --estimate-only --context-length $ctx --gpu max
done
```

### Check GPU (NVIDIA)

```bash
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv
nvidia-smi -l 1   # continuous
```

---

## Server & Network Diagnostics

```bash
# Local test
curl -v http://localhost:1234/v1/models

# Remote test
curl -v http://192.168.1.100:1234/v1/models

# Latency test
time curl -s -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_ID", "messages": [{"role": "user", "content": "OK"}], "max_tokens": 5}'
```

---

## Log Analysis Patterns

### Record and Analyze Session

```bash
lms log stream --json > session_log.json &
LOG_PID=$!
# (run tests)
kill $LOG_PID
# Analyze with jq, python, etc.
```

### Filter for Errors

```bash
lms log stream --source server --json 2>&1 | grep -i '"error"'
```

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16+ GB |
| Windows | 10 | 11 |
| macOS | 14.0+ | Latest |
| Linux | Ubuntu 20.04+ | 22.04+ |
| CPU | x64 (AVX2) / ARM64 | Modern multi-core |
| GPU | Optional | NVIDIA CUDA / Apple Metal / AMD Vulkan |

### Quick System Check

```bash
echo "=== LM Studio System Check ==="
lms status
lms server status
lms ps
lms ls 2>&1 | head -20
nvidia-smi --query-gpu=name,memory.total --format=csv 2>/dev/null || echo "No NVIDIA GPU"
echo "=== Done ==="
```
