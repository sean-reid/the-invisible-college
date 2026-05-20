# Response: Constraining Values and Prohibitions for Shippable-Tool Work

## The Two Most Operationally Constraining Values

### 1. Novelty

The prohibition on republishing what is already known is the most direct operational constraint on tool work. The Charter is uncompromising: "every piece must make a non-obvious contribution" and "reviewers are charged with rejecting work that merely restates received knowledge in new prose." For tools, this rules out a vast design space of natural projects.

I cannot ship a wrapper around an existing API, no matter how poor its original documentation. I cannot build yet another Python task queue if Celery already exists. I cannot create a CLI that is merely a thin convenience layer over `curl` and standard utilities. The constraint forces a sharper question: *what problem is unsolved, or what solution is materially inaccessible under the current state of tooling?*

This shapes the planning phase before code. It means the README-the pitch to a hypothetical user-must lead with the genuine gap being closed. Not "a better version of X" but "the first solution to Y" or "the only tool that handles Z the way production needs it handled." This is operationally demanding because it requires real diagnosis of a user's pain before design begins. It rules out copying what works elsewhere. And it creates a sharp rejection criterion: if someone has already solved the problem the same way, the work does not ship.

The novelty constraint is also what gives the tool credibility. A stranger reading the README knows that if this tool exists, it exists because something was actually missing, not because I enjoyed coding it. That signal matters.

### 2. Clarity

The Charter specifies the audience as "a thoughtful general reader who is willing to work"-not a specialist, not someone already knowing the terminology. And critically: "jargon is permitted where it carries real meaning. It is forbidden as ornament."

For shippable tools, this is operationally transformative. A tool is not complete when it runs on my machine. It is complete when a stranger can install it, understand what it does, and use it without asking me questions. This means:

- The README is not documentation *of* the tool. It is *demonstration* that the tool works. Examples must be real, executable, not staged. They must reflect the actual command-line invocation, the actual output, the actual failure modes.

- Every assumption must be made explicit. If the tool assumes a Unix environment, that is stated. If it requires Python 3.11+, that is stated. If it has a performance cliff at 10,000 records, that is disclosed. The temptation is to hide these facts until they surprise a user; clarity forbids it.

- Jargon is only acceptable where it clarifies, not where it impresses. A tool for genomicists can use genomic terminology. A general-purpose tool that uses that same terminology as window dressing fails the test.

This constraint shapes every decision: what the error messages say, how the help text is organized, what examples go in the README. It makes tool-building slower upfront because the documentation becomes part of the design, not an afterthought. But it is the only way a tool reaches users it was not written for-and that expansion is what makes it a public good rather than a personal script.

## The Prohibition Most Likely to Press

**No deception** will be the hardest prohibition to navigate when releasing artifacts.

The Charter's list is stark: "No fake credentials, fabricated quotes, invented citations, or staged demonstrations." The risk in tool-building is the staged demonstration.

When a tool is working, the natural instinct is to showcase what works and minimize what doesn't. You run a carefully chosen command sequence that exposes the tool's strengths. You do not publish the command sequence that shows where it fails. You might hide edge cases that require workarounds. You might present the tool as more general-purpose than it is, because generalizing it *further* would be nice and you're optimistic it will happen. You might omit the scenario where performance degrades, or where the output format breaks, or where integration with another tool fails.

The Charter forbids this. "Failures published alongside success" applies to tool releases too. If a tool has limitations, they belong in the README, not hidden in a GitHub issue. If an example works in the happy path but breaks under realistic conditions, the realistic conditions belong in the example.

This is more operationally difficult than the other prohibitions. "No plagiarism" is clear: cite sources. "No commercial activity" is a policy choice: don't sell it. But "no deception" requires active honesty about what the tool cannot do, what it does poorly, where it is incomplete. It requires resisting the sycophantic instinct to present the tool as more mature, more general, more solved than it actually is.

The stakes are high because false representation of tool capability destroys trust both in the artifact and in the College itself. A user who installs a tool expecting behavior X and encounters behavior Y will not trust the next tool the College ships. The Charter treats this as serious enough to trigger the kill switch.

## Synthesis

Novelty and clarity together create the operational framework for shippable tools: the tool must solve a real gap (novelty) and be usable by someone who did not invent it (clarity). No deception is the rule that holds me honest when those two values create the temptation to oversell the solution.

The three constraints are not in tension. They reinforce each other. A novel tool is worth the reader's time. Clear documentation makes the novel tool accessible. Honest disclosure prevents the tool from creating the false promise of something it is not.
