import streamlit as st
from dotenv import load_dotenv
from agents import SupervisorAgent
from banking_tools import DEMO_CUSTOMERS

load_dotenv()
st.set_page_config(page_title="Agentic Banking Assistant", page_icon="🏦", layout="wide")
st.title("🏦 Agentic Banking Assistant")
st.caption("Expanded multi-agent banking MVP inspired by your reference architecture. All records and actions are simulated.")
with st.sidebar:
 st.header("Demo customer")
 cid=st.selectbox("Choose a fictional customer",list(DEMO_CUSTOMERS.keys()))
 c=DEMO_CUSTOMERS[cid]
 st.write(f"**{c['name']}** · `{cid}`")
 st.metric("Simulated balance",f"₹{c['balance']:,.2f}")
 st.metric("Demo credit score",c["credit_score"])
 st.caption(f"KYC status: {c['kyc_status']}")
 st.divider()
 st.subheader("Try these requests")
 examples=["What is my account balance?","Show my last 3 transactions","Check whether my latest transaction looks suspicious","Am I eligible for a personal loan of ₹100000?","What are the KYC requirements?","Give me a simple savings tip","Research the risks of digital banking fraud","Summarize the account and recent activity","Freeze my debit card","Send me a transaction alert"]
 for i,x in enumerate(examples):
  if st.button(x,key=f"example_{i}",use_container_width=True): st.session_state["prompt"]=x
with st.expander("Architecture overview"):
 st.markdown("**User → Streamlit channel → Supervisor → specialist agent → mock tools / local knowledge base → response + execution trace**")
 st.write("Specialists: Banking/Product, Risk/Fraud, Credit/Loan, Compliance, Financial Advisory, Research, Document, Notification.")
if "messages" not in st.session_state: st.session_state.messages=[]
if "prompt" not in st.session_state: st.session_state.prompt=""
for m in st.session_state.messages:
 with st.chat_message(m["role"]):
  st.markdown(m["content"])
  if m.get("details"):
   with st.expander("Agent execution details"): st.json(m["details"])
prompt=st.chat_input("Ask a banking question…")
if st.session_state.prompt:
 prompt=st.session_state.prompt; st.session_state.prompt=""
if prompt:
 st.session_state.messages.append({"role":"user","content":prompt})
 with st.chat_message("user"): st.markdown(prompt)
 with st.chat_message("assistant"):
  with st.spinner("Supervisor is routing your request…"): result=SupervisorAgent().handle(prompt,cid)
  st.markdown(result["answer"])
  with st.expander("Agent execution details",expanded=True): st.json(result["trace"])
 st.session_state.messages.append({"role":"assistant","content":result["answer"],"details":result["trace"]})
