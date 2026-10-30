# Refine a story

Bring an agreed story that is not built yet back to ready. Never refine one whose pull request is open or merged: a change then is a question the build asks.

Refine it when it is picked to build or the user asks, and it has no criteria, an open question, examples whose starting code changed on main since it was written, or an answer that now unblocks it. For a backlog, refine only the next few in build order.

1. **Re-read** the story with its comments, its feature's other titles, the spikes and ADRs it waited on, and the code on main with its tests. Find the criteria main already meets, givens main can no longer reach, a rule another story now states, and each break of create.md's rules.
2. **Fix** each in a draft, asking as create.md does:
   * **No criteria:** write them by create.md.
   * **Met already:** delete the criterion. Every one met: close the story with a comment naming the code or test, as a `Decided:` line.
   * **A shared rule:** give it to one story.
   * **Too big:** split it by split.md.
   * **No longer wanted:** ask.
3. **Write it back:** edit the issue through the `tracker` skill and comment what changed, or edit `docs/stories/<slug>.md` and commit it alone.
