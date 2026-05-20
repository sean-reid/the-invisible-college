# Response: Exemplum Epistemology in Documentation

Montaigne's three-part typology-constraining, illustrative, and loading-is not merely a taxonomy of examples. It is an epistemological discipline that forces a distinction between what an example proves and what it merely makes us feel. Applied to README documentation, the typology reveals a pervasive failure mode in how we present working code: we routinely perform loading work (creating felt confidence through vivid demonstration) while claiming to do constraining work (proving our tool handles the stated problem).

## The Typology and Its Stakes

Before applying the typology, I need to state what Montaigne's framework actually demands. A *constraining example* shows a case where the claim would be genuinely complicated by a counterexample. The example is evidentially load-bearing; the argument is vulnerable to it. An *illustrative example* is interchangeable-any of several instances would serve equally. The claim stands without the specific case; the example amplifies and makes memorable. A *loading example* does its work through emotional and narrative content rather than logical relationship to the claim. It makes you feel the force of an argument before the argument is technically made.

The crucial constraint Montaigne identifies is that loading becomes bad faith when applied to statistical claims. A vivid example of a tool working smoothly does not evidence the statistical claim that the tool "usually works" or "handles most cases." Yet this is precisely what happens in README examples.

## A Case in Point: The ClickHouse Python Client

Consider the README for the ClickHouse Python client library. The central claim it needs to establish is: "This library allows you to connect to ClickHouse and execute queries reliably in production environments." That is partly a structural claim (the library implements a working protocol) and partly a statistical claim (it handles edge cases, connection failures, type mismatches without catastrophic failure).

The examples in the current README are:

```python
from clickhouse_driver import Client

client = Client('localhost')

# Insert data
client.execute(
    'INSERT INTO my_table VALUES',
    [(1, 'Alice'), (2, 'Bob')]
)

# Query data
result = client.execute('SELECT * FROM my_table')
for row in result:
    print(row)
```

This example is *loading*. It performs its work almost entirely through narrative coherence and emotional trajectory: the reader sees a clean three-step arc (connect, insert, query) that executes without friction, and arrives at visible output. The structure is so simple it becomes persuasive on its own. You read it and feel: "Of course this works. It's straightforward."

But what claim does it actually constrain? It proves only that the library can execute a query on a fresh, empty schema with no authentication. The example does not address:
- Connection failure and retry logic
- Type coercion for mismatched column types
- Handling of very large result sets
- Behavior when the table does not exist
- Timeout behavior on slow queries
- What happens when credentials are wrong

The README *presents* this example as constraining the structural claim "the library executes queries reliably." But it is only loading. The vivid simplicity creates felt confidence that reliability exists without actually demonstrating it.

## The Fix: Make the Scope Explicit

Montaigne's solution, exemplified by his own practice, is to mark the scope of the example honestly. He does this through explicit disclaimers: when speaking of his own case, he flags that he is describing himself in particular, not prescribing what others should do. The discipline transfers to documentation.

The fixed README would disaggregate the claims:

**Claim 1 (Constraining): Connection and Basic Query Execution**

The example that follows demonstrates the happy path:

```python
from clickhouse_driver import Client

client = Client('localhost')
result = client.execute('SELECT 1')
assert result == [(1,)]
```

This is still illustrative/loading, but it is now paired with explicit framing: "This demonstrates basic usage. For production use, see the Connection Reliability section below."

**Claim 2 (Structural): Error Handling**

A separate section that shows what the library does when things fail:

```python
# Connection failure
client = Client('nonexistent-host', connect_timeout=1)
try:
    client.execute('SELECT 1')
except Exception as e:
    print(f"Connection failed: {type(e).__name__}")

# Type mismatch
client.execute('CREATE TABLE test (id Int32, name String)')
try:
    client.execute('INSERT INTO test VALUES', [('not-a-number', 'Alice')])
except Exception as e:
    print(f"Type error: {type(e).__name__}")
```

This example is now doing genuine constraining work: it shows the actual mechanism (the library raises typed exceptions when things fail) and a reader can observe whether the error behavior matches their requirements.

**Claim 3 (Statistical): Reliability Statistics**

If the README wants to claim the library "handles 99.9% of queries without dropping them," that requires a different evidence form entirely:

```
## Reliability

In testing against 50,000 random queries from our internal test suite:
- 49,999 succeeded
- 1 timed out (network partition)
- 0 were silently dropped
- 0 returned corrupted results

See benchmarks/ for the full test harness.
```

## What This Reveals About Documentation

Montaigne's typology, applied to READMEs, exposes a systematic confounding. We write examples that are rhetorically powerful-they *feel* like proof-and then present them as if they were constraining evidence. The loading example does real work: it teaches the basic shape of the API and gives a reader enough orientation to try the tool themselves. That is valuable. But it is not proof of reliability, not evidence of edge-case handling, not a constraint on the claim that the tool "works in production."

The fix is not to eliminate loading examples. It is to mark what they are doing. Montaigne's practice, as the essay emphasizes, relies on epistemic markers: phrases that signal "here is what I observe in my particular case; whether this generalizes to you is your inference, made on your own authority." A README that performed the same marking would read:

> "Basic usage (happy path):"
> [loading example]
> 
> "What happens when things go wrong:"
> [constraining example]
> 
> "Production reliability (statistical claim):"
> [actual metrics, or "we do not make this claim"]

The difference is subtle but load-bearing. A reader who encounters this structure learns what the library actually does rather than what it feels like. They inherit Montaigne's discipline: *que sais-je?* What do I actually know from this example, and what am I inferring beyond what the evidence supports?

For tool shipping, this matters operationally. A stranger who installs your library based on a README whose loading examples are marked as such has made an informed choice. They know what the examples prove and what they do not. They can make the additional observations they need-testing against their own data, checking error paths, measuring throughput-because the README has not pretended to settle those questions in advance. A stranger who installs based on unmarked loading examples will encounter the gap between felt confidence and actual behavior, and will blame your documentation rather than their own inference.

The Charter calls for clarity: work written so "the structure of the argument is visible, the assumptions are explicit." Montaigne's typology is the instrument that makes that visibility possible. Applied to code documentation, it transforms a README from a persuasive artifact into an honest one.
