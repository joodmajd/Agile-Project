# Team Definition of Done

A story is done only when every applicable item is true:

- Acceptance criteria are met and shown in the running app.
- Code is reviewed by another team member through a pull request; no direct unreviewed change to `main`.
- Unit tests are written first for business rules where practical, then pass locally and in GitHub Actions.
- Relevant Gherkin behavior is added or updated; the agreed BDD runner reports it passing.
- Linter/static analysis reports clean.
- UI handles invalid or incomplete input with a clear message and works at a narrow viewport.
- No real student records, personal phone numbers, or payment data are used.
- README run/test instructions work from a clean checkout.
- Story is linked to Jira, reviewed with the PO, and moved to Done only after acceptance.
- Any known limitation is recorded; changes to behavior or setup are reflected in the docs.

**Evidence:** PR URL/review, CI URL/result, Jira story, test/BDD output, and review acceptance. The team must capture real evidence as it happens; this checklist is not proof that an item has already been completed.
