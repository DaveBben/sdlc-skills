# With no person in the session

* **The work:** the ticket you were given, else the next ready one by the `tracker` skill.
* **Ask a contact** by an issue comment, `Question for @<handle>:`: what the change must do to the product contact, a choice about the code to the engineering contact, else whoever filed it.
* **Wait:** read the issue or pull request every 15 minutes, by the scheduler of the program running you (Claude Code's `/loop 15m`), for up to 8 hours. Then comment what the work waits on, and stop.
* **Report** each result in a comment on the ticket's issue.
