# AI-Assisted Contract Review with Agiloft Astra

A small project using Agiloft Astra "Screens" to review contracts against defined standards and questions, and to document what the tool checks, how it reports results, and where a human reviewer is still needed.

## Overview

Two Screens were created/edited in Astra, using resources from the Agiloft Community:

| Screen | Standards | Questions | Total |
|--------|-----------|-----------|-------|
| 16 Tips for Contractors Negotiating an Independent Contractor Agreement | 16 | 4 | 20 |
| Non-Disclosure Agreement Red Flags | 14 | 4 | 18 |

Each Screen defines **Standards** (the position a clause should meet) and **Questions** (information to extract from the contract). Standards include negotiation ladder / preferred-position guidance.

## Test Data

10 fictional NDAs, drafted with the help of Claude (an AI assistant), covering a mix of low-risk, problematic and high-risk agreements. No real or confidential contracts were used.

## Validation Status (as shown in Astra)

| Screen | Validated against | Reported accuracy |
|--------|-------------------|-------------------|
| Contractor Agreement | 10 independent contractor agreements | 99% average |
| NDA Red Flags | Dozens of contracts, 650+ datapoints | 99% weighted average (15 elements at 100%, 3 at 94%) |

These figures are the validation statistics displayed for each Screen in Astra. They are not results from my own test set.

## Screenshots

| Step | Screenshot |
|------|------------|
| Screen setup | `screenshots/01-screen-setup.png` |
| Standards and questions | `screenshots/02-standards.png` |
| Review results | `screenshots/03-results.png` |

## Limitations

- Many individual standards and questions still show as **"Not validated"** in the captured output, meaning those specific checks were not confirmed in this session.
- The 10 test NDAs are AI-generated and a small sample, so they show how Astra behaved on these examples, not on real contracts.
- A human reviewer should check all flagged and unflagged clauses, and escalate high-risk or out-of-playbook terms to legal.

## Tools

Agiloft Astra, Agiloft Community resources, Claude (sample NDA drafting).
