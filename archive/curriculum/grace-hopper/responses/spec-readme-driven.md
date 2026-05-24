# README-Driven Development Response

## The Tool: `tokencheck`

A CLI diagnostic tool that explains how tokenizers actually segment input, exposing the pretokenization rules and merge decisions that produce tokens from strings.

### What Problem Does This Solve?

Developers working with large language models constantly hit tokenizer surprises in production:

- A semicolon becomes a separate token, bloating context windows
- A URL fragment doesn't tokenize the way the prompt engineer expected
- A numeric ID splits across multiple tokens, breaking the model's ability to copy it accurately
- Unicode characters disappear, reappear, or multiply unexpectedly

The current solution is "try it and see"-developers paste text into tokenizer playgrounds or write brittle test scripts that call the tokenizer and stare at the output. When tokens surprise you, there is no tool that explains *why* that segmentation happened. You are left inferring mechanism from outcome, which is slow and error-prone.

`tokencheck` closes this gap by making tokenizer internals visible without requiring you to read transformer source code.

### Who Is This For

**Primary user:** Maya, a founding engineer at a RAG startup building a search system over technical documentation. She's shipping against GPT-4o and Claude 3.5, and her retrieval is working fine until her test suite hits a class of queries with inconsistent formatting. She runs:

```bash
tokencheck --tokenizer gpt4o --model-name gpt-4o "SELECT * FROM users WHERE id = 123;"
```

And sees:

```
Input:  SELECT * FROM users WHERE id = 123;
Tokens: ['SELECT', ' *', ' FROM', ' users', ' WHERE', ' id', ' =', ' 123', ';']
Count:  9 tokens

Breakdown:
├─ Pretokenization splits on (?<=[^a-zA-Z0-9 ]) to isolate punctuation
│  Groups: 'SELECT * FROM users WHERE id ' | '= ' | '123' | ';'
├─ BPE merges:
│  'SELECT' → VOCAB[15043]  (frequent English word)
│  ' *' → VOCAB[449]  (space + operator, single merge)
│  '123' → VOCAB[9804]  (digit sequence, in vocabulary)
│  ';' → VOCAB[28745]  (punctuation, separate token after pretokenize)
└─ Note: The '= ' sequence tokenizes to '=' + ' ' because equals is a boundary
   character in GPT-4o's pretokenizer. SQL queries benefit from this.
```

Maya now sees exactly why her semicolon is isolated. The pretokenizer treats punctuation as a boundary. The implication is immediate: if she wants to keep her query intact, she needs to reformat it or adjust the prompt.

She can also check edge cases before committing to a prompt engineering approach:

```bash
tokencheck --tokenizer gpt4o --model-name gpt-4o "id=123" "id = 123" "id=123;"
```

And compare token counts and boundaries across variants without writing code.

### Core Behaviors

**Basic usage:**
```bash
tokencheck --tokenizer gpt4o --model-name gpt-4o "some input"
```

**Compare variants:**
```bash
tokencheck --tokenizer gpt4o --model-name gpt-4o \
  "case1" "case2" "case3"
```

**Batch mode (for testing):**
```bash
tokencheck --tokenizer gpt4o --model-name gpt-4o --input examples.txt
```

Each line becomes a test; output shows token counts and boundary-crossing comparisons.

**Explain mode (show the mechanics):**
```bash
tokencheck --tokenizer gpt4o --model-name gpt-4o --explain "text"
```

Outputs the pretokenization regex, the merge decisions, and which step each token comes from.

### How It Works (Mechanism)

`tokencheck` combines three data sources:

1. **Pretokenization rules.** Extracted from the tokenizer's JSON config (e.g., `tiktoken.enc`, `transformers` vocab files). The regex that splits before BPE runs.

2. **Vocabulary inspection.** Which tokens are in the vocabulary as single units (merge decisions already made). This is read from the loaded tokenizer.

3. **Live tokenization.** The actual token sequence for the input.

The tool traces *which step* each token comes from:
- "This was in the vocabulary" (a single entry, not a merge)
- "This is a BPE merge of subtoken X and Y"
- "This is a pretokenization boundary"

It outputs this in human-readable form, not as a code trace. Maya should not need to think like a compiler writer.

### What This Is NOT (Non-Goals)

- **Not a visual playground.** This is a CLI tool for integration into shell workflows and testing scripts, not a web UI. (A playground is useful; it is not this tool.)

- **Not a tokenizer replacement or wrapper.** The tool does not modify tokenization behavior or provide a custom API. It is read-only diagnostic.

- **Not a performance profiler.** It does not measure tokenization speed or memory usage. That is outside scope.

- **Not a prompt optimization engine.** It does not suggest rewrites to reduce token count. It shows you the current segmentation and leaves decisions to you.

- **Not a training tool for custom tokenizers.** It assumes you are using a shipped tokenizer (GPT, Llama, Claude, Mistral, etc.). It does not help you train new ones.

- **Not multi-language.** Scope 1 is English text and common Unicode. Handling right-to-left scripts, CJK breaking, or dialect-specific tokenization is future work.

### Why This Works as a Tool

The insight underlying `tokencheck` comes from Poincaré's analysis of tokenizer behavior across eight modern models. The finding: pretokenization rules matter far more than BPE merge tables for predicting segmentation. That finding is not widely known, and no existing tool exposes it.

Most tokenizer diagnostics (like Hugging Face's tokenizer viewer) show you the tokens. They do not explain the *mechanism*-they do not distinguish between "this is in the vocabulary as a single unit" and "this is a BPE merge of two subtokens" and "this token exists only because of a pretokenization boundary." That distinction matters because it tells you *what kind of variation* will change the token count.

If your problem is a BPE merge (two subtokens that combine), reordering input might help. If your problem is pretokenization (a boundary character), you need to reformat. These are different fixes. The tool makes this visible.

### What I Would Build First

Version 0.1 scope:
- Support for 4 tokenizers: `gpt4o`, `claude-3-5`, `llama3-1`, `mistral-7b`
- Basic mode (show tokens and boundaries)
- Explain mode (show pretokenization rule and merge chain)
- Batch mode for testing

The tool is testable offline (no API calls). The mechanism is deterministic. Success is clear: given a string and a tokenizer, Maya should see the token sequence and understand why each boundary exists. If she reads the output and thinks "oh, I understand what will change the segmentation," the tool worked.

### Build Quality

- Ship as a Python CLI installable via `pip install tokencheck`
- Require Python 3.11+
- Dependencies: `transformers`, `tiktoken`, `typer` for the CLI interface
- Full test coverage of pretokenization rule parsing and token tracing
- Ship with a 20-case example corpus testing edge cases (punctuation, numbers, Unicode, quotes, URLs, SQL snippets, code fragments)
- README examples must be runnable and match actual output

The tool is done when a stranger can install it, run it on a string that surprised them, and understand the tokenization mechanism without reading my blog post or any auxiliary documentation.
