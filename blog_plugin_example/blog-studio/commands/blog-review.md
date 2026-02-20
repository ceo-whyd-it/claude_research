---
description: Review an existing local file against the strict blog rules.
args:
  - name: filename
    description: The name of the file to review (e.g., 'tokenizers-intro.md')
---

# Review Existing Blog Post

Please activate the `editorial-manager` agent.

Tell the manager: "I want to review the file named {{filename}}. Please read it from the filesystem, validate the frontmatter with the astro-validator, and then run the Strict Editor protocol."
