# Forecast a set of stories

* **Count stories; never convert points to days.**
* **Throughput** is stories finished per week over the last 6 to 10 weeks, from the tracker or from merges in `git log`. Say which, and how many weeks.
* **Report a range:** `N stories left; a median of M a week over the last W weeks; about X weeks at even odds, Y weeks at 85 in 100.` With 10 or more weeks of history, resample the weekly counts (Monte Carlo). With fewer, give the slowest and fastest week's range and call it rough.
* **Raise N by the split rate so far** (stories added since the start over stories at the start), or say none is known yet.
* **A spike** adds its timebox to the calendar, not a story to the count.
* **No history,** or weeks mostly zero or swinging widely: give no forecast. Offer an appetite (Shape Up): the person's time budget, and which stories fit it in map order.
