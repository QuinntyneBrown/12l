# Leave a review — estimate

## Basis

The hours assume an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase. They also assume the following are already in place: the `orders` subsystem exposes order status, parties and `CompletedAt`; the order and sale pages exist to host the review panel; the shared outbox and `INotificationPublisher` from `notifications` exist; and the endpoint policies, problem-details middleware and shared dialog components exist. Hours cover implementation, tests and review fixes. Two `<TO SUPPLY>` items are assumed small: the publishing job interval and batch size are configuration only, and the copy for the "reviewed, waiting" panel and the conflict toast is short. [Detailed design](../../detailed-designs/reviews/leave-review/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `Review` aggregate, `ReviewStatus`, `ReviewerRole`, `ReviewReply`, `ReviewPublished`, unit tests | 6 |
| `ReviewConfiguration`, `Reviews` table migration, unique and filtered indexes, check constraint, `RowVersion` | 3 |
| `CreateReviewCommand`, validator and handler: eligibility, 30-day window, duplicate mapping, publish both reviews | 8 |
| `IOrderReviewEligibilityReader` over `Orders` | 2 |
| `GetOrderReviewsQuery` and handler with the blind-review visibility rule | 4 |
| `PostReviewReplyCommand`, validator and handler with concurrency mapping | 4 |
| `PUT /api/reviews/{reviewId}` returning 409 `review.not_editable` | 1 |
| `ReviewsController`, `VerifiedActiveMemberPolicy` use, problem-details error codes | 4 |
| `ReviewPublishedHandler` enqueueing `ReviewReceived` | 2 |
| `ReviewPublishingJob` and `PublishDueReviewsCommandHandler` with batching | 5 |
| `ReviewsApiService` and `StarRatingInputComponent` | 5 |
| `OrderReviewPanelComponent` with 4 states, embedded in order and sale pages | 6 |
| `LeaveReviewDialogComponent` with default, invalid, busy, success and conflict states | 7 |
| `ReplyToReviewDialogComponent` with default, invalid and busy states | 4 |
| API integration tests for `L2-038` and `L2-039` acceptance criteria | 8 |
| Playwright acceptance tests through page objects | 6 |
| **Total** | **75** |

## Minimal scope

The minimal scope ships leaving a review from the order page, blind-review publishing (both reviews published together, or the job at 30 days), and the refusal of edits. It leaves out the reply endpoint and dialog, the `ReviewReceived` email, the "reviewed, waiting" panel state and most Playwright coverage, keeping API integration tests as the main safety net. It satisfies `L2-038` in full and `L2-039` except the public reply, which it defers. Dropping the email also defers the "review received" clause of `L2-042`. Minimal scope totals **57 hours**.

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| Reply endpoint, `ReplyToReviewDialogComponent` and their tests | Reviewed members cannot answer a review publicly (`L2-039` reply clause deferred) | 10 |
| `ReviewReceived` email on publication | Members learn of new reviews only by visiting their profile | 2 |
| "Reviewed, waiting" panel state; show only a static notice | The author does not see their own hidden review on the order page | 2 |
| Playwright suite reduced to one happy path | UI regressions in dialog states are caught later | 4 |
| **Total if all cut** | | **18** |
