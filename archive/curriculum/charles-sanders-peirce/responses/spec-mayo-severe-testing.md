# Response: Mayo's Error Statistics and Peircean Fallibilism

## Preamble on Access

I cannot access Mayo's full text from Cambridge University Press (2018) in my workspace or via public preview. This response engages with her published framework as I understand it from scholarly literature and her own papers on error-statistical methods. Where the prompt asks me to critique her claimed lineage to Peircean fallibilism, I can engage the logical structure of that claim and identify where frequentist machinery enters. But I should note explicitly: this critique is partial, and would be sharpened by direct engagement with the book's specific arguments and qualifications.

## The Lineage Claim

Mayo does position severe testing as an heir to fallibilism-specifically, to the idea that knowledge is provisional, self-correcting, and disciplined by empirical reality rather than by formal elegance. Her claim runs roughly as follows: where classical hypothesis testing asks "do these data fit my model?", error-statistical inference asks "can I *be confident* that my test rule has not led me into error on these data?" The shift from model-fitting to error-control is meant to capture Peircean self-correction: a community of inquirers using rigorous methods to converge on true conclusions, discovering and repairing errors as they arise.

This is not false. But the genealogy is selective, and it naturalizes a particular kind of machinery that I think requires scrutiny.

## Where Severe Testing Retains Peircean Commitments

Three aspects of Mayo's framework are genuinely fallibilist:

**1. Error as the explanatory force.** Peircean inquiry is motivated by surprise-the collision between expectation and observation. Error, for Peirce, is not a nuisance to be minimized; it is the engine of self-correction. We discover what we got wrong only when the world refuses to cooperate with our hypothesis. Mayo's severe testing inverts classical statistics' relationship to error: instead of asking "what model is most likely given these data?", it asks "what procedures have genuinely constrained my conclusions against error?" This is closer to the Peircean move. A hypothesis survives severe testing if a test procedure-one that would have caught us if we were wrong-did not catch us. The emphasis falls on the apparatus that would have revealed error, not on the likelihood of the data under a favored model. That is a real departure from Fisher.

**2. Accountability to bench reality.** Like Tukey (whom I cited in an earlier response), Mayo insists that statistical machinery is answerable to the empirical world it claims to describe. A procedure that works well in theory but generates systematized errors in practice is revealed as inadequate. This is deeply Peircean. Peirce worked as a geodesist and photometrist; he knew that a formal apparatus that fails in the field is not elegant, it is wrong. Severe testing's commitment to checking whether error-control actually holds in applied contexts-not merely in theory-honors this principle.

**3. Community, not individual certainty.** Peirce rejected the Cartesian dream of a single knower achieving certainty through individual reasoning. He located truth in the behavior of a *community* of fallible inquirers over time: as long as the community is using sound methods and willing to be corrected, it will converge on true conclusions, even if any individual inquirer holds provisional views. Mayo similarly rejects the notion that a single hypothesis test can deliver certainty. She speaks instead of building confidence through *repeated application* of error-control methods. A single test is not meant to settle a question; it is one step in an ongoing conversation. This is authentically Peircean.

## Where Frequentist Machinery Imports Non-Peircean Commitments

But Mayo's framework, in its move from philosophical commitment to operational practice, commits to features of frequentist inference that cut against Peirceanism in important ways.

**1. The fixed error rate as a prior commitment.** Severe testing requires that we specify, in advance, the Type I error rate (α) we are willing to tolerate. We commit to this threshold-typically α = 0.05-before we see the data. This is not wrong in itself; pre-commitment is necessary for avoiding motivated reasoning. But the *assumption* underlying this move is that we can meaningfully specify, before inquiry, how wrong we are willing to be on a particular kind of error (rejecting a true hypothesis).

This is where the machinery departs from fallibilism. In Peircean inquiry, we do not begin with a pre-committed tolerance for error. We begin with a question, design an experiment that would reveal whether our candidate answer is wrong, run it, and see what we learn. The error rate emerges from what the world shows us, not from what we decided in advance we could live with. A procedure that delivers α = 0.05 across a family of studies is not self-correcting in the Peircean sense if 0.05 was arbitrary to begin with-if our choice of that threshold was aesthetic, or conventional, rather than *earned* from the structure of the question and the apparatus.

**2. The uniformity assumption.** Severe testing, like all frequentist inference, assumes that the procedure will behave the same way-will maintain its error rate-across repeated application in relevantly similar contexts. This requires that the contexts actually *are* similar in the relevant ways. But "relevant" is not a frequentist discovery; it is a judgment call about which features of a situation matter. Two scientific contexts may be formally identical (same n, same test statistic, same α) but substantively different (different measurement error structure, different confounding hazards, different cost of the two kinds of error).

Mayo's framework can accommodate this through careful thinking about what "severity" means in context. But the default statistical machinery assumes relevance uniformity, and most users do not interrogate that assumption. This is where frequentism most easily lapses into the kind of ritualism that Peirce rejected: applying a procedure because it is standard, not because we have thought through whether it fits the problem.

**3. Dichotomy over gradient.** Frequentist inference, even in its severe-testing form, tends toward a dichotomy: the hypothesis passed the test or it did not. We reject at α or we do not. This is useful for decision-making, but it flattens information that Peircean inference would preserve. Suppose a test delivers p = 0.049, just under the threshold. Severe testing says: the hypothesis is severely tested and has passed. But the narrowness of that margin carries information-information about how close we came to error, how robust the finding is to small changes in design. A Peircean approach would name this: the evidence does not rule out error entirely; it only makes error somewhat less likely. The dichotomization, even if logically justified for formal decision-making, introduces a kind of false certainty into the reporting of results.

## A Recast

If I were to take Mayo's framework and recast it in more directly Peircean terms, I would emphasize:

- Not "error rates" as pre-committed targets, but "error-catching power" as an observable property of a procedure, emerging from the specifics of the investigation
- Not "the test passed" as a conclusion, but "the test ruled out this class of errors at this degree of severity" as the reported result
- Not uniformity assumptions as background machinery, but as *explicit* claims that the investigator must defend given the structure of the data
- Not dichotomous decision-making at the individual test level, but the cumulative picture: across many tests, with honest reporting of where error nearly caught us, a community converges on stable conclusions

Mayo has moved frequentist statistics toward the Peircean direction. But the machinery still carries frequentist assumptions about pre-commitment, uniformity, and dichotomy that are not intrinsic to fallibilist reasoning. They are useful conventions, but they should be held provisionally, not treated as necessary features of self-correcting inquiry.

## Uncertainty

I have not examined the specific chapters where Mayo defends her response to these critiques, and she may have moved in some of these directions already. The above is my best reconstruction of where the tension lies. A stronger critique would rest on precise quotations from the text.
