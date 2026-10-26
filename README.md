# Agentic Banking Assistant — Expanded MVP

A Streamlit demo with a supervisor/orchestrator and eight specialist agents. All data is fictional. It does not connect to a real bank.

## Use cases
1. Account balance and profile
2. Recent transactions
3. Rule-based fraud-risk flags
4. Illustrative personal-loan eligibility estimate
5. KYC/compliance information
6. General savings education
7. Research using a local keyword-retrieval knowledge base
8. Simulated account activity summary
9. Simulated debit card freeze
10. Simulated notification log

## Architecture mapping to the reference
- **Channel:** Streamlit chat UI.
- **Experience layer:** input handling and chat session state.
- **AI control plane:** optional LLM intent classification plus safe rule-based fallback.
- **Orchestrator:** `SupervisorAgent` routes requests.
- **Agent layer:** Banking/Product, Risk/Fraud, Credit/Loan, Compliance, Financial Advisory, Research, Document, Notification.
- **Tool layer:** mock Python functions in `banking_tools.py`.
- **Enterprise-style data:** fictional customer and transaction dictionaries.
- **Knowledge/RAG prototype:** small local keyword-based retrieval over banking notes (not a vector database).
- **Production layers:** OAuth, API gateway, MCP gateway, real external services, observability and human approval are documented as future work, not implemented.

## Windows setup
Open the extracted folder containing `app.py` and `requirements.txt` in VS Code. Open Terminal → New Terminal:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
If `.venv` is already activated, do not recreate it; run install/start commands from the folder containing `requirements.txt`. If that file is not found, use `dir` and `cd` to the folder that contains it. Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Optional LLM
Copy `.env.example` to `.env`, add an OpenAI API key, and restart. Never upload `.env` or your API key to GitHub. Without a key, deterministic rules keep the application usable. The LLM only classifies intent; Python tools perform the data operations.

## Demo prompts
- What is my account balance?
- Show my last 3 transactions
- Check whether my latest transaction looks suspicious
- Am I eligible for a personal loan of ₹100000?
- What are the KYC requirements?
- Give me a simple savings tip
- Research the risks of digital banking fraud
- Summarize the account and recent activity
- Freeze my debit card
- Send me a transaction alert

## Safety and limitations
No real bank, credit bureau, KYC provider, SMS/email service or payment network is connected. Card freeze and notifications are local simulations. Fraud checks are simple rules, not a trained model. Loan EMI is an illustrative proxy, not a real EMI calculation or credit decision. Knowledge retrieval is keyword based, not embeddings/vector search. There is no production authentication, database, or audit service.

## GitHub submission
```bash
git init
git add app.py agents.py banking_tools.py requirements.txt README.md ARCHITECTURE.md .env.example .gitignore
git commit -m "Build multi-agent banking assistant MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/agentic-banking-mvp.git
git push -u origin main
```
Never commit `.env`, keys, or real customer information.

## Demo video outline (5–10 min)
Intro and simulation disclaimer; explain architecture; test balance, transactions, fraud, loan, KYC, savings, account summary, notification and card freeze; show agent trace; explain LLM/fallback; finish with limitations and future work.
