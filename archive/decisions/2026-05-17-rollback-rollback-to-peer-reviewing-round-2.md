---
kind: rollback
recorded_at: 2026-05-17T22:47:32+00:00
actors: [founder]
project: 2026-05-17-when-the-same-sum-gives-different-answer-4da4
---

# Rollback to peer_reviewing round 2
A bug in _existing_reviews_in_round (the round filter was missing from the SQL) made peer_review.run() see all round-1 reviewers as already-done for round 2, so the project transitioned to editorial without any round-2 reviews. The function has been fixed. This rollback restores the project to peer_reviewing (round 2) so the three round-2 reviews can be filed as intended.
