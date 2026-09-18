# Archived contract versions

Retired versions of the four canonical contracts. **Read-only and append-only.**

A file here is named `<id>@<version>.md` and is the sole source for that one
retired version, exactly as the file it replaced is the sole source for the
current one. `atj release-check` refuses a file that restates a current version,
is named for a version it does not contain, or no longer parses.

Nothing here governs new work. `atj validate reports` accepts an artifact that
pins an archived version and reports it as an advisory, so a completed event's
record stays valid and stays legible as history. `canon.load_reference()` reads
these files when a completed event's numbers are recomputed, so a total is always
checked against the criteria that were actually in force when it was judged.

Editing a file in this directory rewrites the past of every event that pins it.
