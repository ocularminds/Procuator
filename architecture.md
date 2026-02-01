┌─────────────────────────────────────────────────────────────────────┐
│                     PROCUREMENT DECISION AGENT                       │
│   Trigger: New purchase request (email/form/webhook)                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────────┐  ┌─────────────────────┐     │
│  │   STEP 1    │  │     STEP 2      │  │       STEP 3        │     │
│  │ Parse Input │──▶ Extract Entities│──▶ Enrich with Context │     │
│  │             │  │                 │  │                     │     │
│  └─────────────┘  └─────────────────┘  └──────────┬──────────┘     │
│         │                  │                       │                │
│         ▼                  ▼                       ▼                │
│  ┌─────────────┐  ┌─────────────────┐  ┌─────────────────────┐     │
│  │  Skill:     │  │   Skill:        │  │    Skill:           │     │
│  │ Document AI │  │  NER &          │  │   Fetch Supplier    │     │
│  │             │  │ Classification  │  │   Profile from DB   │     │
│  └─────────────┘  └─────────────────┘  └─────────────────────┘     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                             DECISION POINT                           │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    AI Reasoning Step                         │    │
│  │  Input: Supplier profile, amount, category, request context  │    │
│  │  Model: groq/openai/gpt-oss-120b                              │    │
│  │  Prompt: "Evaluate risk and policy compliance. Consider:     │    │
│  │          - Supplier risk score: {score}                      │    │
│  │          - Amount vs budget: {amount}/{budget_remaining}     │    │
│  │          - Category approval rules: {rules}                  │    │
│  │          Output: APPROVE/REFER/DENY with confidence % and    │    │
│  │          reasoning."                                          │    │
│  └──────────────┬──────────────────────────────────────────────┘    │
│                 │                                                   │
│         ┌───────┴──────────┐                                       │
│         ▼                  ▼                  ▼                    │
│  ┌─────────────┐  ┌─────────────────┐  ┌─────────────────────┐     │
│  │  APPROVE    │  │     REFER       │  │       DENY          │     │
│  │  Pathway    │  │   Pathway       │  │     Pathway         │     │
│  └──────┬──────┘  └────────┬────────┘  └──────────┬──────────┘     │
│         │                  │                       │                │
│         ▼                  ▼                       ▼                │
│  ┌─────────────┐  ┌─────────────────┐  ┌─────────────────────┐     │
│  │ Skill:      │  │   Skill:        │  │    Skill:           │     │
│  │ Send to     │  │ Create Review   │  │   Send Rejection    │     │
│  │ Payment     │  │ Ticket in       │  │   with Policy       │     │
│  │ System      │  │ ServiceNow      │  │   Citation          │     │
│  └─────────────┘  └─────────────────┘  └─────────────────────┘     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                           AUDIT & FEEDBACK                          │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                     Log Decision                             │    │
│  │  Skill: Write to Audit Database with:                        │    │
│  │  - Request ID, decision, confidence, reasoning, timestamp    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                   Collect Feedback (Optional)               │    │
│  │  Skill: Send follow-up to requester: "Was this decision     │    │
│  │  helpful?" → Improve prompts/policies over time             │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
