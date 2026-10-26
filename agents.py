"""Supervisor/orchestrator and eight specialist agents."""
import os, re
from banking_tools import *

def money(v): return f"₹{v:,.2f}"

class BankingAgent:
 name="Customer / Banking Product Agent"
 def run(self,intent,cid,prompt):
  c=get_customer(cid)
  if intent=="balance":
   d=get_balance(cid); return f"{c['name']}, your simulated balance is **{money(d['balance'])}**.",{"tool":"get_balance","result":d}
  if intent=="transactions":
   m=re.search(r"last\s+(\d+)",prompt.lower()); limit=min(int(m.group(1)),10) if m else 5
   ts=get_transactions(cid,limit)
   return "Recent simulated transactions:\n"+"\n".join(f"- {t['date']} · **{t['merchant']}** · {money(t['amount'])} · {t['city']} · `{t['id']}`" for t in ts),{"tool":"get_transactions","count":len(ts)}
  if intent=="profile":
   return f"**Account summary**\n\n- Name: {c['name']}\n- Customer ID: {cid}\n- Account: {c['account_type']}\n- KYC: {c['kyc_status']}\n- Card: {get_card_status(cid)}\n- Balance: {money(c['balance'])}",{"tool":"get_customer"}
  if intent=="freeze_card":
   d=freeze_card(cid); return "**Simulated debit card frozen.** No real card was changed.",{"tool":"freeze_card","result":d}
  docs=search_knowledge(prompt)
  return "**Banking information**\n\n"+"\n\n".join(f"- **{d['title']}**: {d['text']}" for d in docs),{"tool":"search_knowledge","matches":len(docs)}

class RiskFraudAgent:
 name="Risk / Fraud Agent"
 def run(self,cid):
  t=get_latest_transaction(cid); c=get_customer(cid); flags=[]
  if abs(t["amount"])>=10000: flags.append("large transaction amount")
  if t["city"]!=c["usual_city"]: flags.append("unusual city")
  verdict="⚠️ **Flagged for review**" if flags else "✅ **No obvious flags found**"
  return f"Latest transaction `{t['id']}` at **{t['merchant']}** for **{money(t['amount'])}** in {t['city']}: {verdict}.\n\nReason: {', '.join(flags) if flags else 'amount and location pass simple demo rules'}. Not a real fraud decision.",{"tool":"get_latest_transaction","transaction_id":t["id"],"risk_flags":flags}

class CreditLoanAgent:
 name="Credit / Loan Agent"
 def run(self,cid,prompt):
  m=re.search(r"(?:₹|rs\.?\s*)?([\d,]+)",prompt.lower()); amount=int(m.group(1).replace(",","")) if m else 100000
  amount=max(10000,min(amount,5000000)); d=assess_loan(cid,amount)
  status="potentially eligible" if d["eligible"] else "not eligible"
  return f"Under the fictional demo policy, you are **{status}** for **{money(amount)}**.\n\n- Demo credit score: {d['credit_score']}\n- New EMI proxy: {money(d['estimated_new_emi'])}\n- Total EMI / income: {d['estimated_total_emi_ratio']}%\n- Reason: {d['reason']}\n\nNot a real approval or financial advice.",{"tool":"assess_loan","result":d}

class ComplianceAgent:
 name="Compliance Agent"
 def run(self,cid,prompt):
  d=get_kyc_status(cid); docs=search_knowledge("KYC identity documents")
  return f"**Demo KYC status:** {d['status']}\n\n**General checklist:** {docs[0]['text'] if docs else 'Confirm with your bank.'}",{"tool":"get_kyc_status","result":d}

class FinancialAdvisoryAgent:
 name="Financial Advisory Agent"
 def run(self,cid,prompt):
  d=search_knowledge("savings budget financial")
  return "**General financial education**\n\n"+(d[0]["text"] if d else "Track expenses and set a realistic savings goal."),{"tool":"search_knowledge","topic":"savings"}

class ResearchAgent:
 name="Research Agent"
 def run(self,cid,prompt):
  d=search_knowledge(prompt) or search_knowledge("digital banking fraud security")
  return "**Research notes from the local knowledge base**\n\n"+"\n\n".join(f"- **{x['title']}**: {x['text']}" for x in d),{"tool":"search_knowledge","matches":len(d)}

class DocumentAgent:
 name="Document Agent"
 def run(self,cid,prompt):
  c=get_customer(cid); ts=get_transactions(cid,5)
  credits=sum(t["amount"] for t in ts if t["amount"]>0); debits=sum(abs(t["amount"]) for t in ts if t["amount"]<0)
  return f"**Simulated activity summary**\n\n- Customer: {c['name']} (`{cid}`)\n- Transactions: {len(ts)}\n- Credits in sample: {money(credits)}\n- Debits in sample: {money(debits)}\n\nNot an official bank statement.",{"tool":"get_transactions","count":len(ts)}

class NotificationAgent:
 name="Notification Agent"
 def run(self,cid,prompt):
  t=get_latest_transaction(cid); msg=f"Demo alert: transaction {t['id']} at {t['merchant']} for {money(t['amount'])}."
  d=log_notification(cid,msg)
  return f"**Simulated notification created:** {msg}\n\nStatus: {d['status']}. Nothing was sent externally.",{"tool":"log_notification","result":d}

class SupervisorAgent:
 def classify_with_rules(self,p):
  p=p.lower()
  if any(x in p for x in ["fraud","suspicious","risk","scam","phishing"]): return "fraud"
  if any(x in p for x in ["loan","eligible","credit score","emi"]): return "loan"
  if any(x in p for x in ["freeze","block my card","block card"]): return "freeze_card"
  if any(x in p for x in ["transaction","statement","spending","payment history"]): return "transactions"
  if any(x in p for x in ["kyc","aml","compliance","identity document"]): return "compliance"
  if any(x in p for x in ["savings tip","save money","budget","financial planning","financial advice"]): return "advisory"
  if any(x in p for x in ["research","market","digital banking"]): return "research"
  if any(x in p for x in ["summarize","summary","document","account activity","report"]): return "document"
  if any(x in p for x in ["notification","alert","notify","send me"]): return "notification"
  if any(x in p for x in ["balance","how much money","available money"]): return "balance"
  if any(x in p for x in ["profile","account details","my account"]): return "profile"
  return "product" if any(x in p for x in ["product","account type","savings account","insurance","cards"]) else "help"
 def classify_with_llm(self,prompt):
  if not os.getenv("OPENAI_API_KEY"): return None
  try:
   from openai import OpenAI
   client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
   r=client.chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),temperature=0,messages=[
    {"role":"system","content":"Classify request into exactly one label: balance, transactions, fraud, loan, freeze_card, profile, product, compliance, advisory, research, document, notification, help. Return only label. Simulated banking app."},
    {"role":"user","content":prompt}])
   label=r.choices[0].message.content.strip().lower()
   return label if label in {"balance","transactions","fraud","loan","freeze_card","profile","product","compliance","advisory","research","document","notification","help"} else None
  except Exception: return None
 def handle(self,prompt,cid):
  intent=self.classify_with_llm(prompt); method="LLM" if intent else "rule-based fallback"
  intent=intent or self.classify_with_rules(prompt)
  bank=BankingAgent()
  if intent in {"balance","transactions","profile","freeze_card","product","help"}: agent=bank; out=agent.run(intent,cid,prompt)
  elif intent=="fraud": agent=RiskFraudAgent(); out=agent.run(cid)
  elif intent=="loan": agent=CreditLoanAgent(); out=agent.run(cid,prompt)
  elif intent=="compliance": agent=ComplianceAgent(); out=agent.run(cid,prompt)
  elif intent=="advisory": agent=FinancialAdvisoryAgent(); out=agent.run(cid,prompt)
  elif intent=="research": agent=ResearchAgent(); out=agent.run(cid,prompt)
  elif intent=="document": agent=DocumentAgent(); out=agent.run(cid,prompt)
  else: agent=NotificationAgent(); out=agent.run(cid,prompt)
  answer,detail=out
  return {"answer":answer,"trace":{"supervisor":"Supervisor / Agent Orchestrator","intent":intent,"routing_method":method,"agents_called":[agent.name],"tool_result":detail}}
