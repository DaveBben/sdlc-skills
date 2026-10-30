# Large refactorings

Keep the build releasable at every step by trunk-based development: each step its own pull request, merged before the next starts:

* **Parallel change** for an interface.
* **Branch by abstraction** for a dependency.
* **Strangler fig** for a subsystem.
* **The Mikado method** when the prerequisites are unknown.
* **Hundreds of mechanical edits:** write a codemod or script, not hand edits.
