"""Fictional banking data and mock tools. No real bank is connected."""
from datetime import date

DEMO_CUSTOMERS = {
 "C1001":{"id":"C1001","name":"Aarav Sharma","account_type":"Savings","balance":125000.0,"credit_score":742,"monthly_income":65000,"existing_monthly_emi":8000,"usual_city":"Chennai","card_status":"Active","kyc_status":"Verified"},
 "C1002":{"id":"C1002","name":"Meera Iyer","account_type":"Salary","balance":38500.5,"credit_score":668,"monthly_income":42000,"existing_monthly_emi":12000,"usual_city":"Chennai","card_status":"Active","kyc_status":"Pending"}
}
TRANSACTIONS = {
 "C1001":[
  {"id":"TXN-501","date":"2026-10-20","merchant":"FreshMart","amount":-1250,"type":"Debit","city":"Chennai"},
  {"id":"TXN-500","date":"2026-10-19","merchant":"Salary Credit","amount":65000,"type":"Credit","city":"Chennai"},
  {"id":"TXN-499","date":"2026-10-18","merchant":"Metro Cafe","amount":-340,"type":"Debit","city":"Chennai"},
  {"id":"TXN-498","date":"2026-10-17","merchant":"Online Electronics","amount":-18999,"type":"Debit","city":"Bengaluru"},
  {"id":"TXN-497","date":"2026-10-16","merchant":"Utility Bill","amount":-2100,"type":"Debit","city":"Chennai"}],
 "C1002":[
  {"id":"TXN-601","date":"2026-10-20","merchant":"Grocery Store","amount":-950,"type":"Debit","city":"Chennai"},
  {"id":"TXN-600","date":"2026-10-19","merchant":"Salary Credit","amount":42000,"type":"Credit","city":"Chennai"},
  {"id":"TXN-599","date":"2026-10-18","merchant":"Online Gaming","amount":-7800,"type":"Debit","city":"Mumbai"}]
}
CARD_OVERRIDES = {}
NOTIFICATION_LOG = []
KNOWLEDGE_DOCS = [
 {"title":"KYC checklist","tags":"kyc identity documents compliance","text":"KYC commonly requires identity proof, address proof, a recent photograph, and forms requested by the bank. Requirements vary; confirm through official channels."},
 {"title":"Digital banking safety","tags":"fraud security scam phishing research","text":"Never share OTPs, PINs, passwords, or full card details. Use official banking apps, verify recipients, and report unfamiliar transactions through official support."},
 {"title":"Savings basics","tags":"savings budget save financial planning","text":"Track essential expenses, set realistic savings goals, maintain an emergency fund, and review recurring subscriptions. This is general education, not personalized advice."},
 {"title":"Loan basics","tags":"loan emi credit eligibility","text":"Loan eligibility can depend on income, existing obligations, credit history, loan amount, and lender policy. This demo estimate is not a credit decision."},
 {"title":"Complaint escalation","tags":"complaint help support dispute","text":"For real banking issues, contact the bank through its official app or website. Keep transaction IDs and never share passwords or OTPs."}
]
def get_customer(cid): return DEMO_CUSTOMERS.get(cid)
def get_balance(cid):
 c=get_customer(cid); return {"customer_id":cid,"balance":c["balance"],"currency":"INR"} if c else None
def get_transactions(cid,limit=5): return TRANSACTIONS.get(cid,[])[:max(0,min(limit,10))]
def get_latest_transaction(cid):
 rows=get_transactions(cid,1); return rows[0] if rows else None
def get_card_status(cid): return CARD_OVERRIDES.get(cid,DEMO_CUSTOMERS[cid]["card_status"])
def freeze_card(cid):
 CARD_OVERRIDES[cid]="Frozen"; return {"customer_id":cid,"card_status":"Frozen","simulated":True}
def assess_loan(cid,amount):
 c=get_customer(cid)
 if not c: return {"eligible":False,"reason":"Customer not found"}
 emi=amount*0.02
 ratio=(c["existing_monthly_emi"]+emi)/c["monthly_income"]
 reasons=[]
 if c["credit_score"]<650: reasons.append("credit score below demo threshold 650")
 if ratio>0.35: reasons.append("estimated total EMI exceeds 35% of income")
 return {"eligible":not reasons,"requested_amount":amount,"credit_score":c["credit_score"],"monthly_income":c["monthly_income"],"estimated_new_emi":round(emi,2),"estimated_total_emi_ratio":round(ratio*100,1),"reason":"Meets demo checks" if not reasons else "; ".join(reasons)}
def get_kyc_status(cid):
 c=get_customer(cid); return {"status":c["kyc_status"],"customer_id":cid} if c else None
def search_knowledge(query):
 words=set(query.lower().replace("?","").split())
 rows=[]
 for d in KNOWLEDGE_DOCS:
  corpus=set((d["title"]+" "+d["tags"]+" "+d["text"]).lower().split())
  score=len(words & corpus)
  if score: rows.append((score,d))
 rows.sort(key=lambda x:x[0],reverse=True)
 return [{"title":d["title"],"text":d["text"],"score":s} for s,d in rows[:3]]
def log_notification(cid,message):
 item={"customer_id":cid,"message":message,"status":"Simulated / not sent","date":date.today().isoformat()}
 NOTIFICATION_LOG.append(item); return item
