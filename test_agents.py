import unittest
from banking_tools import get_balance, get_transactions, assess_loan
from agents import SupervisorAgent

class SmokeTests(unittest.TestCase):
 def test_balance(self): self.assertEqual(get_balance("C1001")["balance"],125000.0)
 def test_transaction_limit(self): self.assertEqual(len(get_transactions("C1001",3)),3)
 def test_loan_schema(self): self.assertIn("eligible",assess_loan("C1001",100000))
 def test_fraud_routing(self): self.assertEqual(SupervisorAgent().classify_with_rules("check suspicious transaction"),"fraud")
 def test_kyc_routing(self): self.assertEqual(SupervisorAgent().classify_with_rules("what are KYC requirements"),"compliance")
if __name__=="__main__": unittest.main()
