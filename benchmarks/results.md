# Day 20 Lab — Numbers Scratchpad

## Hardware

- Platform: Windows 11 (AMD64)
- CPU: Intel Core i7-8750H (6 physical · 12 logical cores)
- RAM (GB): 15.9 GB
- GPU/accelerator: NVIDIA GeForce GTX 1050 (running CPU only)
- llama.cpp build backend: CPU

## Track 01 — Quickstart

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|---:|---:|---:|---:|---:|
| qwen2.5-1.5b-instruct-q4_k_m.gguf | 1068 | 126 / 172 | 36.4 / 39.7 | 2420 / 2542 / 2556 | 27.5 |
| qwen2.5-1.5b-instruct-q2_k.gguf | 379 | 180 / 207 | 28.5 / 31.0 | 2003 / 2093 / 2109 | 35.1 |

**One observation:** Q2_K quantization provides a nice speed boost (~27%) but Q4_K_M is much more reliable for complex tasks.

## Track 02 — llama-server load test

| Concurrency | RPS | TTFB P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Failures |
|--:|--:|--:|--:|--:|--:|
| 10 | 0.28 | 23000 | 41000 | 41000 | 0 |
| 50 | 0.21 | 22000 | 44000 | 44000 | 0 |

**KV-cache observation:** peak `llamacpp:kv_cache_usage_ratio` from `record-metrics.py` was 0.09 at concurrency 50, which means we are far from cache limits, but CPU-bound.

## Track 03 — Milestone Integration

- N16 piece used: stub
- N17 piece used: stub
- N18 piece used: stub
- N19 piece used: TOY_DOCS
- One-paragraph reflection: Most latency is in the LLM call. Retrieve is sub-millisecond.

## Bonus — llama.cpp optimization

### Thread comparison
| threads | tg128 (tok/s) |
|--:|--:|
| 6 | 23.9 |
| 12 | 27.5 |

### The one change that mattered most
Using 12 threads instead of 6 provided a 15% speedup on this machine.
