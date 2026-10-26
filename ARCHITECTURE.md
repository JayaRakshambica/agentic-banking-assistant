# Architecture and design decisions

Flow: `User → Streamlit UI → Supervisor/Orchestrator → Specialist Agent → Mock Tool / Local Knowledge → Answer + Trace`

The app demonstrates the reference diagram's UI/channel, light experience layer, intent-routing control plane, orchestrator, specialist agents, mock tool layer, fictional enterprise-style data, and basic knowledge retrieval.

The optional LLM returns only a constrained intent label. If no API key is set or the call fails, rule-based classification is used. Specialist agents call Python functions rather than asking the LLM to invent balances or execute actions. An execution trace displays the selected intent, routing method, agent, and tool output.

Specialists: Customer/Banking Product, Risk/Fraud, Credit/Loan, Compliance, Financial Advisory, Research, Document, Notification.

Not implemented: real API Gateway/WAF/OAuth, MCP gateway, vector database/embeddings, live core banking or credit bureau, external notification services, production identity/access controls, persistent audit logs, human approval workflow, and monitoring. These require additional infrastructure and are out of scope for a short MVP.

Future improvements: database and migrations, authentication/RBAC, audit logs, unit/integration tests, embedding-based RAG, approved sandbox APIs, human confirmation for sensitive actions, model evaluation and monitoring.
