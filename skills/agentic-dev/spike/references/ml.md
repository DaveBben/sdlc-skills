# An ML or eval experiment

One run on one seed proves little, and a number with nothing beside it proves nothing. The finding is the comparison, on data the model never saw while you chose its settings.

* **Put a baseline beside every number:** the plain approach the decision weighs against, such as the current prompt, the previous model, the majority class or a keyword rule, through the same eval.
* **Fix the splits before the first run:** train, validation and test. Choose settings on validation only, and read the test split once, at the end. A setting tuned on the test split has passed an exam it already saw.
* **Keep related rows on one side of a split:** split by customer, document or time where rows share one, so nothing leaks from train into test.
* **Run several seeds,** 3 unless the person states more, and report the mean and the spread. A difference inside the spread is no difference.
* **Pick the metric the decision needs:** with imbalanced classes, never accuracy alone. Check that a degenerate output, such as a constant or the majority class, scores badly on it.
* **Know who labelled the sample,** and check a few labels against each other before trusting a score on them.
* **Read real outputs,** 20 at least, failures included: a metric can rise for the wrong reason.
* **Pin everything a rerun needs:** the data snapshot or its hash, the model and library versions, the seed, the config and the prompt text.
* **Spend the compute budget the person stated,** in GPU-hours, runs or dollars, and track it as you go. Answer with the smallest model and the least data that can, and check in when the budget is spent.
* **Record each run** in the finding: its config, seed, metric and cost.
