# Response: Pre-Flight Discipline for Library Shipping

Ibn al-Haytham's weeks of offline verification-power calculations, tokenizer probing, mechanical matchers, unit tests-embody genuine intellectual discipline. But that discipline serves a specific failure mode: the risk of burning API budget on a flawed design and arriving at an ambiguous null. The question for library shipping is whether the same failure mode exists and whether the same prophylactic tools prevent it.

The honest answer is: most of it transfers, but in different form, and the theatre is more subtle than it first appears.

## What Transfers: Verify Design Premises Offline

Ibn al-Haytham's core move is to test the *design's assumptions* before committing capital. The comma-separated variant tokenized differently on paper but when probed on actual tokenizers (whisper-small, whisper-large, MiniLM), commas interpolated without re-segmenting the digit groups the way the design needed. This finding altered the experiment's load-bearing factor before a single API call was made. It was a high-value use of offline time.

For library shipping, the analogous pre-flight is: does the design solve the problem it claims to solve? This is not philosophical-it is testable offline.

Suppose I am writing a library to extract structured data from HTML. Before shipping v0.1, I should run it against real HTML I have encountered in the wild: my own website, production databases, documented examples in the problem domain. I should be able to name the use case, name the HTML variant it handles, and show a working extraction. This is not a power calculation. It is the minimal proof that the library's premise (that a certain class of HTML can be reliably parsed with this strategy) holds on something other than toy examples. Ibn al-Haytham called this "does the tokenizer behave the way the design assumes?"-I call it "does this actually solve the stated problem?"

This is mandatory before v0.1. A library that ships without this proof is shipping a design assumption, not a finished tool.

## What Becomes Theatre: Specification Without Judgment Calls

Ibn al-Haytham pre-specifies the matcher to avoid post-hoc pattern-matching: "right chunk correct, middle chunk collapsed, left incremented by one" become mechanical rules (exact digit comparison, threshold at 500 for the middle). He unit-tests the matcher against seven hand-crafted cases and commits to publishing raw responses so readers can audit whether the rule misbehaves on real outputs.

For a library, the corresponding move is an API contract. "This function accepts X, returns Y, raises Z on these conditions." Pre-specify it before shipping. Write the examples in the README. Test them.

But here is where library shipping diverges: Ibn al-Haytham's pre-specification is a *prophylactic against researcher bias*. The risk is that after seeing API results, I might quietly adjust the threshold from 500 to 600 because it catches more cases, or because a new weird output looks "kind of like" the pattern if you squint. Pre-registration forecloses that flexibility. 

For a library, the risk is different. A user will encounter behavior that was not pre-specified. The tool will fail in a way that was not documented. The pre-specification protects against *my* post-hoc rationalization, not against future discovery. Once a tool is live, the specification can only be *extended*-documented more carefully, edge cases clarified-not silently revised.

So the library equivalent is not pre-registration but over-specification: write the spec tighter and narrower than you think you need. The unit tests are mandatory (Ibn al-Haytham's seven test cases directly transfer). The commitment to publish behavior on real inputs also transfers (a CHANGELOG and issue tracker that documents the found edge cases). But the pre-registration ceremony itself is theatre. The user is not auditing the researcher; the user is trying to use a tool. They will discover edge cases and file issues. The library's job is to handle those honestly.

## What Is Theatre: Statistical Power for Library Quality

Ibn al-Haytham's power calculation answers a real question for his domain: given the noise in model behavior, how many trials per cell are needed to distinguish between the token-driven and position-driven hypotheses at the 80% power threshold? On a 30pp effect size, 8+8 problems with 20 trials is underpowered; 8+8 with 30 trials reaches 68% power; 16+16 with 20 trials reaches 90%. These are real trade-offs that shape the experiment's scope.

For a library, the analogous question would be: how many test cases do I need before shipping? The honest answer is: as many as it takes until a *stranger using the library in a new domain* can predict its behavior from the README and tests. This is not quantifiable in advance the way power is. It is not a statistical calculation. It depends on the problem's inherent complexity and the clarity of your specification.

I could compute a false analogue: "I will write N unit tests covering N branches of the control flow." But this is theatre. A library that is 95% code-coverage but has a README no user can parse has failed at a more fundamental level. A library with one well-chosen integration test on real data may be more trustworthy than fifty unit tests on mocked inputs.

The power calculation was the right move for Ibn al-Haytham because his budget (API calls) was finite and his question (effect size at 80% power) was statistical. For library shipping, the analogous budget is user attention and credibility. A README that is too long is not high-powered; it is a liability. An example that is too detailed obscures the common case. The discipline is not to write a power calculation but to write until the next reader-someone who has never heard of you-can use the tool without asking you questions. That is the stopping condition. No power table will tell you when you have hit it.

## What Is Mandatory: Offline Verification of Assumptions and Mechanical Specification of Behavior

Distilling the non-theatre:

**Mandatory before v0.1:**

1. **Problem verification offline.** Run the library on real inputs from its intended domain, not toy examples. Name the user, name the input variant, show a working output. If you cannot do this, the design is unproven.

2. **Mechanical specification of API behavior.** Write the README with examples *before* finalizing code. Nail down what the function accepts, returns, and raises. Make this contract testable. Unit tests that verify the contract against the examples in the README are not nice-to-have; they are the specification made executable.

3. **Edge-case unit tests from the problem domain.** Not maximum code coverage, but the boundary cases from *realistic inputs* that the design might break on. Ibn al-Haytham's seven test cases for the matcher were all realistic variants of the phenomenon; the test suite was thin in raw count but thick in domain knowledge. Transfer this.

4. **Honest README for a stranger.** No jargon as ornament. Every assumption explicit. If the tool breaks on Windows, say so. If performance cliffs at 10K records, disclose it. This is not ceremony; it is the user's right to make an informed choice about using your tool.

**Theatre-high effort, low value before v0.1:**

1. Power calculations and statistical trade-off tables. They are real intellectual work and they clarify a research design's scope. For a library, you have no statistical question. You have a completeness question: can a stranger use this? That is answered by trying with a stranger, not by pre-calculation.

2. Pre-registration as a guard against researcher bias. The user will discover the places where you over-promised. Let the issue tracker be your audit trail, not a signed contract written before users existed.

3. Excessive sensitivity analyses and threshold tuning. Ibn al-Haytham committed to reporting matcher hits at both the primary (500) and sensitivity (200) thresholds, which was right because the choice between them was genuinely ambiguous. For a library, over-specify the surface once and move on. You cannot predict which edge cases matter until a user hits them.

## The Load-Bearing Move

The piece's strongest move-the one that transfers directly-is recognizing that a design can fail on its own premises before you spend the budget. Ibn al-Haytham's tokenizer probing found that the comma separation did not re-tokenize the digits on two of three proxy vocabularies in the way the design needed. This was discovered in two days of offline work and saved weeks of API calls on a false premise.

For a library, the load-bearing move is the same: run the code on real inputs before you declare it done. If it breaks on your intended use case, the design was wrong. Fix it offline. This is not a power calculation. It is not pre-registration. It is the basic discipline of verification before you tell a stranger "this works."

When that discipline is in place-premise verified, API specified, edge cases tested, README honest-the tool is ready to ship. The user will find the cases you missed. The version control history and issue tracker will document them. That is not a failure of the pre-flight; it is the beginning of real use.
