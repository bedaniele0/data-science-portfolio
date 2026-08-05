from __future__ import annotations

import argparse
import asyncio
import statistics
import time

import httpx
from sklearn.datasets import load_breast_cancer


def sample_payload() -> dict[str, list[float]]:
    dataset = load_breast_cancer(as_frame=True)
    X = dataset.data.copy()
    X["radius_area_ratio"] = X["mean radius"] / (X["mean area"] + 1e-6)
    return {"features": X.iloc[0].tolist()}


async def send_requests(url: str, total_requests: int, concurrency: int) -> tuple[list[float], float]:
    payload = sample_payload()
    latencies: list[float] = []
    semaphore = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient(timeout=30.0) as client:
        async def one_call() -> None:
            async with semaphore:
                start = time.perf_counter()
                response = await client.post(url, json=payload)
                response.raise_for_status()
                latencies.append((time.perf_counter() - start) * 1000)

        started = time.perf_counter()
        await asyncio.gather(*[one_call() for _ in range(total_requests)])
        total_time = time.perf_counter() - started
    return latencies, total_time


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark local serving API.")
    parser.add_argument("--url", default="http://127.0.0.1:8000/predict")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=10)
    args = parser.parse_args()

    latencies, total_time = asyncio.run(
        send_requests(url=args.url, total_requests=args.requests, concurrency=args.concurrency)
    )
    p95 = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies)
    throughput = args.requests / total_time if total_time else 0.0
    print(f"requests={args.requests}")
    print(f"concurrency={args.concurrency}")
    print(f"avg_latency_ms={statistics.mean(latencies):.2f}")
    print(f"p95_latency_ms={p95:.2f}")
    print(f"throughput_rps={throughput:.2f}")


if __name__ == "__main__":
    main()

