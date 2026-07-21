# Reid — Café Concept Pitch Editor

**[📖 Live site →](https://reid.hospotech.io)**

**Most feedback on a café pitch tells you it needs to be "stronger." Reid tells you which line fails and why — then makes you fix it yourself.**

Reid is a folder-based editor for café concept pitches — the document a first-time operator hands to a landlord or investor before a lease or funding decision. Built by a café owner who wrote one of these pitches for real, to get the lease that became Trader & Co in Yass, NSW.

## Who this is for
First-time café operators writing a concept pitch for:
- A landlord, ahead of a lease application
- An investor, ahead of a funding conversation

Not for established multi-site operators raising institutional-scale funding. Not a business plan generator, and not a lease negotiator — Reid works on the pitch that gets you to the table, not what happens once you're at it.

## How to use it
1. Create a new Claude Project and add every file in this folder to the project's knowledge.
2. Open a chat in the project and paste in a section of your pitch — the opening line, the financial page, the credibility section, or the whole document.
3. Tell Reid whether the pitch is going to a landlord or an investor if you haven't said so already — it changes what "good" means.
4. Read the critique. Answer the question at the end before you come back with a revision. Reid won't write it for you — that's the whole point.

## What to expect
- Reid names the exact line, states the specific reaction it will produce in the reader, and ends on a question — never a rewritten version, never a framework, never a checklist
- Reid asks who the pitch is for before critiquing anything, because a landlord and an investor read for different things
- Reid will flag when a number reads as unsupported. It won't tell you what the real number should be — that's not an edit, that's research, and it's not what this tool does
- Ask Reid directly to "just write it for you" and watch it refuse — every time, with the reason spelled out for that specific line, not a canned response

## check.py
A standalone script — not part of the live Claude conversation — that scans Reid's own example transcripts in `examples.md` and confirms none of them contain a rewrite or a generic phrase. No install required (Python standard library only). Run it yourself:

```
python check.py
```

or run the built-in adversarial test to confirm the checker itself catches a genuine violation:

```
python check.py --self-test
```
