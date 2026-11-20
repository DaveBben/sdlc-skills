# Forecast a set of stories

For "how long will this take" asked about several stories, usually for a manager.

* **Count stories; never convert points to days.** A count means something only when stories are about one size, which one merge request each gives.
* **Throughput** is stories finished per week over the last 6 to 10 weeks, from the tracker or from merged merge requests in `git log`. Say which, and how many weeks.
* **Report a range:** `N stories left; a median of M a week over the last W weeks; about X weeks at even odds, Y weeks at 85 in 100.` With 10 or more weeks of history, resample the weekly counts (Monte Carlo) for the two figures. With fewer, give the range from the slowest and fastest week and call it rough.
* **Split allowance:** stories get split after they are counted. Raise N by the split rate so far, stories added since the start over stories at the start, or say none is known yet.
* **A spike** adds its timebox to the calendar, not a story to the count.
* **No forecast yet:** with no history, or weeks that are mostly zero or swing widely, say so. Offer an appetite instead: the person names a time budget and you show which stories fit it, in map order. Forecast again once 3 stories have merged.
