# Reflection — Lab 20 (Personal Report)

> **Đây là báo cáo cá nhân.** Mỗi học viên chạy lab trên laptop của mình, với spec của mình. Số liệu của bạn không so sánh được với bạn cùng lớp — chỉ so sánh **before vs after trên chính máy bạn**. Grade rubric tính theo độ rõ ràng của setup + tuning của bạn, không phải tốc độ tuyệt đối.

---

**Họ Tên:** Phan Anh Ly Ly
**Cohort:** A20-K1
**Ngày submit:** 2026-05-07

---

## 1. Hardware spec (từ `00-setup/detect-hardware.py`)

- **Platform :** Windows 11 Home 23H2 (AMD64)
- **CPU      :** Intel Core i7-9750H
- **Cores    :** 6 physical · 12 logical cores
- **RAM      :** 15.9 GB
- **GPU      :** nvidia_cuda - NVIDIA GeForce GTX 1050, 4096 MiB
- **llama.cpp backend:** CPU (fallback from CUDA due to Windows App Control policy)
- **Recommended model:** Qwen2.5-1.5B-Instruct (Q4_K_M)

**Setup story** (≤ 80 chữ): Tôi gặp lỗi App Control policy khi load `llama.dll` bản CUDA từ wheel prebuilt, nên đã fall back sang bản CPU-only wheel. Tôi cũng phải fix script `detect-hardware.py` vì lệnh `wmic` không nhận diện được RAM trên một số bản Windows 11 mới, thay bằng PowerShell `Get-CimInstance`.

---

## 2. Track 01 — Quickstart numbers (từ `benchmarks/01-quickstart-results.md`)

Settings: `n_threads=12`, `n_ctx=2048`, `n_batch=512`, `n_gpu_layers=99`.

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|---:|---:|---:|---:|---:|
| qwen2.5-1.5b-instruct-q4_k_m.gguf | 1068 | 126 / 172 | 36.4 / 39.7 | 2420 / 2542 / 2556 | 27.5 |
| qwen2.5-1.5b-instruct-q2_k.gguf | 379 | 180 / 207 | 28.5 / 31.0 | 2003 / 2093 / 2109 | 35.1 |

**Một quan sát** (≤ 50 chữ): Q4_K_M chậm hơn Q2_K khoảng 20-30% nhưng chất lượng câu trả lời mạch lạc hơn hẳn. Trên CPU, bottleneck chính là memory bandwidth nên Q2_K (nhẹ hơn) cho throughput cao hơn.

---

## 3. Track 02 — llama-server load test

| Concurrency | Total RPS | TTFB P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Failures |
|--:|--:|--:|--:|--:|--:|
| 10 | 0.28 | 23000 | 41000 | 41000 | 0 |
| 50 | 0.21 | 22000 | 44000 | 44000 | 0 |

**KV-cache observation** (từ `record-metrics.py`): peak `llamacpp:kv_cache_usage_ratio` ở concurrency 50 = 0.09, nghĩa là server chỉ mới dùng 9% dung lượng cache (2048 tokens). Với concurrency cao, bottleneck nằm ở compute (CPU) xử lý queue thay vì tràn bộ nhớ cache.

---

## 4. Track 03 — Milestone integration

- **N16 (Cloud/IaC):** stub: localhost only
- **N17 (Data pipeline):** stub: in-memory dict
- **N18 (Lakehouse):** stub: in-memory toy data
- **N19 (Vector + Feature Store):** stub: TOY_DOCS keyword matching

**Nơi tốn nhiều ms nhất** trong pipeline:

- embed: 0 ms (skipped)
- retrieve: 0.1 ms
- llama-server: 3285.4 ms

**Reflection** (≤ 60 chữ): Bottleneck chính xác nằm ở `llama-server` (chiếm >99% latency). Việc dùng CPU serving khiến prefill và decode cực chậm. Trong thực tế, cần offload sang GPU hoặc dùng quantization mạnh hơn/model nhỏ hơn để giảm latency.

---

## 5. Bonus — The single change that mattered most

**Change:** Thử nghiệm thay đổi `n_threads` từ 6 (physical cores) lên 12 (logical cores).

**Before vs after** (paste 2-3 dòng từ sweep output):

```
n_threads=6:  23.9 tok/s
n_threads=12: 27.5 tok/s
speedup: ~1.15×
```

**Tại sao nó work**:
Mặc dù deck khuyên dùng `n_threads = physical_cores` để tránh overhead của hyperthreading, trên máy tôi dùng 12 threads lại nhanh hơn 15%. Có thể do model 1.5B quá nhỏ để bão hòa memory bandwidth chỉ với 6 cores, hoặc kiến trúc i7-8750H hưởng lợi từ việc parallelize các operation nhỏ trên nhiều logical cores hơn.

---

## 6. (Optional) Điều ngạc nhiên nhất

Tôi ngạc nhiên khi thấy việc patch code `llama-cpp-python` để thêm endpoint `/metrics` lại đơn giản đến vậy nhờ FastAPI. Điều này cho thấy tính linh hoạt của các công cụ serving hiện đại.

---

## 7. Self-graded checklist

- [x] `hardware.json` đã commit
- [x] `models/active.json` đã commit
- [x] `benchmarks/01-quickstart-results.md` đã commit
- [x] `benchmarks/02-server-results.md` (hoặc CSV từ `record-metrics.py`) đã commit
- [x] `benchmarks/bonus-*.md` đã commit (thực tế dùng `results.md` ghi lại thread comparison)
- [x] Ít nhất 6 screenshots trong `submission/screenshots/`
- [x] `make verify` exit 0
- [x] Repo trên GitHub ở chế độ **public**
- [x] Đã paste public repo URL vào VinUni LMS
