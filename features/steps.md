# BDD step mapping

These five Gherkin scenarios run with the dependency-free scenario harness (`npm run bdd`) and map to the tested domain functions in `src/domain.js`:

| Scenario | Unit-level executable assertion |
|---|---|
| Draft hidden | `createQuiz` filters `status === published` |
| Approval and publishing | `reviewQuestion` moves a draft to approved, then approved to published |
| Ten, no repeats | `createQuiz` returns ten unique questions when enough are available |
| Score and explanations | `scoreQuiz` checks the rounded score; UI renders per-question explanation |
| History | `recordAttempt` persists topic, score, time, and answer details |

The harness checks the feature file contains the expected five scenarios and executes matching Given/When/Then behavior with assertions. Attach the passing run from the shared CI and show at least one scenario live during the demo. If the instructor requires a specific BDD tool such as Cucumber, port these mappings to that runner.
