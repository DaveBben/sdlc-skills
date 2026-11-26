# A performance or load spike

A benchmark on a laptop with toy data measures the laptop. The finding holds only for the data, environment and load it ran on, so state them and how they differ from production.

* **Use production-shaped data at production size,** in an environment like production's: hardware, network, database size and concurrent users.
* **Report percentiles,** p50, p95, p99 and the maximum, never the mean alone.
* **Separate warm from cold:** discard warm-up runs, and report a cold start on its own where it matters.
* **Run it several times** and report the spread; a difference inside the noise is no difference.
* **Change one thing at a time,** through the same harness for every approach.
* **Profile before you optimise:** name the bottleneck from a profile, not a guess.
* **Ramp a load test to the stated load,** and watch errors and saturation (CPU, memory, connections, queue depth), not latency alone.
* **Ask before loading a shared or production system.**
* **Timebox in time.**
