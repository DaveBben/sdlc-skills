# A performance or load spike

A benchmark on a laptop with toy data measures the laptop. The finding holds only for the data, environment and load it ran on, so state them and how they differ from production.

* **Use production-shaped data at production size,** in an environment like production's: hardware, network, database size and concurrent users.
* **For client code, the environment is the slowest supported device and network:** a throttled mid-range phone, the minimum-spec PC or console, a packaged build rather than the editor or dev server. Report frame time in milliseconds with 1% lows and hitches, not average fps.
* **Measure the optimised release build.** For a microbenchmark use the language's harness, such as criterion, Google Benchmark, JMH, BenchmarkDotNet or pytest-benchmark, so the compiler cannot remove the work and warm-up is handled.
* **Report percentiles,** p50, p95, p99 and the maximum, never the mean alone.
* **Separate warm from cold:** discard warm-up runs, and report a cold start on its own where it matters.
* **Change one thing at a time.**
* **When the question is where the time goes,** answer from a profile, not a guess.
* **Ramp a load test to the stated load,** and watch errors and saturation (CPU, memory, connections, queue depth), not latency alone.
* **Ask before loading a shared or production system.**
* **Timebox in time.**
