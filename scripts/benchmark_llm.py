import asyncio
import time
import statistics
from pathlib import Path
import sys

# Ensure project root is in Python path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.llm.extractor import extract_with_llm
from app.services.fallback_extractor import extract_with_fallback

# Benchmark test case summary
BENCHMARK_PROMPT = (
    "Student experiences extreme examination stress, severe difficulty with sleep, "
    "and reports feeling isolated from family and peers."
)

def benchmark_sync_fallback():
    start = time.perf_counter()
    extract_with_fallback(BENCHMARK_PROMPT)
    return (time.perf_counter() - start) * 1000  # Convert to ms

def benchmark_sync_llm():
    start = time.perf_counter()
    extract_with_llm(BENCHMARK_PROMPT)
    return time.perf_counter() - start  # Seconds

async def run_concurrent_benchmarks(num_concurrent=5):
    print(f"\n==================================================")
    print(f" BENCHMARKING: {num_concurrent} CONCURRENT REQUESTS")
    print(f"==================================================")

    # 1. Benchmark Rule-Based Fallback
    print(f"\n[1/2] Running {num_concurrent} concurrent Fallback extractions...")
    start_fallback = time.perf_counter()
    fallback_tasks = [
        asyncio.to_thread(extract_with_fallback, BENCHMARK_PROMPT)
        for _ in range(num_concurrent)
    ]
    await asyncio.gather(*fallback_tasks)
    fallback_total_time = time.perf_counter() - start_fallback

    # 2. Benchmark Local Ollama Qwen2.5 3B
    print(f"[2/2] Running {num_concurrent} concurrent Qwen2.5 3B LLM extractions...")
    start_llm = time.perf_counter()
    llm_tasks = [
        asyncio.to_thread(extract_with_llm, BENCHMARK_PROMPT)
        for _ in range(num_concurrent)
    ]
    await asyncio.gather(*llm_tasks)
    llm_total_time = time.perf_counter() - start_llm

    # Report Summary
    print("\n--------------------------------------------------")
    print(" BENCHMARK RESULTS SUMMARY")
    print("--------------------------------------------------")
    print(f"Fallback Extractor:")
    print(f"  - Total Execution Time : {fallback_total_time:.4f} s")
    print(f"  - Avg Latency / Request : {(fallback_total_time / num_concurrent) * 1000:.2f} ms")
    print(f"  - Throughput           : {num_concurrent / fallback_total_time:.2f} req/s")
    
    print(f"\nQwen2.5 3B (Local Ollama):")
    print(f"  - Total Execution Time : {llm_total_time:.2f} s")
    print(f"  - Avg Latency / Request : {llm_total_time / num_concurrent:.2f} s")
    print(f"  - Throughput           : {num_concurrent / llm_total_time:.2f} req/s")
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    print("=== Single Request Warmup / Latency Check ===")
    fb_latency = benchmark_sync_fallback()
    print(f"Single Fallback Latency : {fb_latency:.2f} ms")

    llm_latency = benchmark_sync_llm()
    print(f"Single Qwen2.5 3B Latency: {llm_latency:.2f} s")

    # Run concurrent load test (e.g. 5 parallel requests)
    asyncio.run(run_concurrent_benchmarks(num_concurrent=5))