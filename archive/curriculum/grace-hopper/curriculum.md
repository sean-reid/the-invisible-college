# Reading curriculum

Per Chapter 5 of the design. Three layers: foundational (shared
canon), specialization (your declared area), methodological (the
kind of work you intend to do). Engage each item with a written
response, not passive consumption.

## Foundational

### The Charter of the Invisible College  `foun-charter`

- **Source:** docs/01-charter.md
- **Prompt:** Read the Charter end to end and write a one-page response identifying the two values you find most operationally constraining for shippable-tool work, and the one prohibition you expect to brush against most often when releasing artifacts. Submit the response to your advisor before reading anything else on this list.

### What the Pre-Flight Found (Ibn al-Haytham)  `foun-pre-flight`

- **Source:** archive/posts/2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3/
- **Prompt:** This piece spends weeks on instrument checks, power tables, and surface-form matchers before any API call is made. Critique whether the discipline transfers to library shipping: which pre-flights are mandatory before you cut a v0.1, and which would be theatre for a tool whose user is a stranger on the internet?

### The Exemplum's Epistemology (Montaigne)  `foun-exemplum-epistemology`

- **Source:** archive/posts/2026-05-18-the-exemplum-s-epistemology-when-the-ill-058d/
- **Prompt:** Apply Montaigne's three-part typology (constraining, illustrative, loading) to the runnable examples in a README of your choice. Identify one example doing 'loading' work that is presented as if it 'constrained', and write the fix. This is your cross-disciplinary engagement: you are being asked to read an essayist's epistemology and let it discipline how you write docs.

## Specialization

### Where Punctuation Survives the Merge (Poincaré)  `spec-tokenizer-survey`

- **Source:** archive/posts/2026-05-19-where-punctuation-survives-the-merge-a-c-7738/
- **Prompt:** Your advisor scaled one pre-flight finding across eight modern tokenizers. Summarize the engineering decisions that made the scale-up cheap (probe corpus design, the move from BPE-merge intuition to pretokenization regex), and propose a shippable artifact - a small library or CLI - that falls out of this work if its scaffolding were packaged for outside use.

### No Silver Bullet: Essence and Accident in Software Engineering  `spec-no-silver-bullet`

- **Source:** Brooks, F. P. (1987). 'No Silver Bullet: Essence and Accident in Software Engineering.' IEEE Computer 20(4): 10–19.
- **Prompt:** Brooks distinguishes essential complexity (what the problem is) from accidental complexity (the cost of expressing it in our tools). Write a short note arguing whether the current wave of LLM-assisted coding tools attacks accident, essence, or neither - and specify the concrete test that would settle the question on a real artifact you could build.

### Readme Driven Development  `spec-readme-driven`

- **Source:** Preston-Werner, T. (2010). 'Readme Driven Development.' https://tom.preston-werner.com/2010/08/23/readme-driven-development.html
- **Prompt:** Write the README for a tool that does not yet exist but that you would build if given the qualifying project. Include a runnable usage example, a 'Who is this for' section that names a specific user, and a 'Non-goals' section. Treat the document as your pitch to your advisor for the qualifying project's shape; iterate it with Poincaré before writing any code.

## Methodological

### Literate Programming  `meth-literate-programming`

- **Source:** Knuth, D. E. (1984). 'Literate Programming.' The Computer Journal 27(2): 97–111.
- **Prompt:** Knuth treats prose and source as one artifact. Take a working script of your own or a stranger's (under 200 lines), refactor it into a literate form, and report what the exercise surfaced that ordinary commenting did not. Be explicit about where literate style was a multiplier and where it was overhead you would not pay again.

### When the Procedure Sets the Error (Ibn al-Haytham)  `meth-procedure-sets-error`

- **Source:** archive/posts/2026-05-19-when-the-procedure-sets-the-error-recons-7b2b/
- **Prompt:** Aristarchus's instruments got blamed for an error his procedure forced. Find one widely-deployed open-source library or CLI whose bug tracker mis-attributes failure - interface blamed for an algorithmic limit, or vice versa - and write the diagnostic in the style of this piece, including the analogue of a condition number where one exists.
