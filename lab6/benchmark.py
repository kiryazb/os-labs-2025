#!/usr/bin/env python3
import argparse
import random
import statistics
import sys
import time
from typing import List

from algorithms import selection_sort_linked_list, selection_sort_list
from data_structures import LinkedList


def generate_data(size: int, rng: random.Random) -> List[int]:
    return [rng.randint(0, size * 10) for _ in range(size)]


def is_sorted_list(values: List[int]) -> bool:
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def is_sorted_linked(ll: LinkedList) -> bool:
    current = ll.head
    while current and current.next:
        if current.value > current.next.value:
            return False
        current = current.next
    return True


def benchmark_structures(
    sizes: List[int], trials: int, seed: int, verify: bool
) -> List[dict]:
    rng = random.Random(seed)
    results = []
    for size in sizes:
        base_data = generate_data(size, rng)
        list_times: List[float] = []
        linked_times: List[float] = []
        for _ in range(trials):
            data_for_list = list(base_data)
            start = time.perf_counter()
            sorted_list = selection_sort_list(data_for_list)
            list_times.append(time.perf_counter() - start)
            if verify and not is_sorted_list(sorted_list):
                raise AssertionError("List version produced unsorted result")

            ll = LinkedList.from_iterable(base_data)
            start = time.perf_counter()
            sorted_ll = selection_sort_linked_list(ll)
            linked_times.append(time.perf_counter() - start)
            if verify and not is_sorted_linked(sorted_ll):
                raise AssertionError("LinkedList version produced unsorted result")
        results.append(
            {
                "size": size,
                "array_mean": statistics.mean(list_times),
                "array_stdev": statistics.stdev(list_times) if trials > 1 else 0.0,
                "linked_mean": statistics.mean(linked_times),
                "linked_stdev": statistics.stdev(linked_times) if trials > 1 else 0.0,
            }
        )
    return results


def print_table(results: List[dict]) -> None:
    print(f"{'N':>8} | {'Array mean (s)':>15} | {'Linked mean (s)':>16}")
    print("-" * 46)
    for row in results:
        print(
            f"{row['size']:8d} | "
            f"{row['array_mean']:15.6f} | "
            f"{row['linked_mean']:16.6f}"
        )


def maybe_plot(results: List[dict], output: str) -> None:
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except ModuleNotFoundError:
        print("matplotlib not installed; skipping plot.", file=sys.stderr)
        return

    sizes = [row["size"] for row in results]
    array_times = [row["array_mean"] for row in results]
    linked_times = [row["linked_mean"] for row in results]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, array_times, marker="o", label="ArrayList")
    plt.plot(sizes, linked_times, marker="o", label="LinkedList")
    plt.xlabel("Dataset size (N)")
    plt.ylabel("Time, s")
    plt.title("Selection sort timings")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    print(f"Plot saved to {output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark selection sort on ArrayList vs LinkedList"
    )
    parser.add_argument(
        "--sizes",
        default="100,500,1000,2000,4000",
        help="Comma-separated dataset sizes",
    )
    parser.add_argument("--trials", type=int, default=3, help="Trials per size")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Save a matplotlib plot to selection_sort_timings.png if matplotlib is available",
    )
    parser.add_argument(
        "--plot-path",
        default="selection_sort_timings.png",
        help="Path for the generated plot",
    )
    parser.add_argument(
        "--no-verify",
        action="store_false",
        dest="verify",
        help="Skip correctness check that outputs are sorted",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sizes = [int(value) for value in args.sizes.split(",") if value]
    results = benchmark_structures(sizes, args.trials, args.seed, args.verify)
    print_table(results)
    if args.plot:
        maybe_plot(results, args.plot_path)


if __name__ == "__main__":
    main()
