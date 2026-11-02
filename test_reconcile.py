
import unittest
from reconcile import reconcile


class TestReconciliation(unittest.TestCase):

    def setUp(self):
        self.expected = [
            {
                "transaction_id": "TXN1001",
                "amount": "25.50",
                "expected_status": "APPROVED"
            }
        ]

        self.processed = [
            {
                "transaction_id": "TXN1001",
                "amount": "25.50",
                "status": "APPROVED"
            }
        ]

    def test_successful_transaction(self):
        issues = reconcile(self.expected, self.processed)
        self.assertEqual(issues, [])

    def test_missing_transaction(self):
        issues = reconcile(self.expected, [])
        self.assertIn(
            ["TXN1001", "MISSING TRANSACTION"], issues
        )

    def test_amount_mismatch(self):
        self.processed[0]["amount"] = "30.00"
        issues = reconcile(self.expected, self.processed)
        self.assertIn(
            ["TXN1001", "AMOUNT MISMATCH"], issues
        )

    def test_status_mismatch(self):
        self.processed[0]["status"] = "DECLINED"
        issues = reconcile(self.expected, self.processed)
        self.assertIn(
            ["TXN1001", "STATUS MISMATCH"], issues
        )

    def test_duplicate_transaction(self):
        self.processed.append(self.processed[0].copy())
        issues = reconcile(self.expected, self.processed)
        self.assertIn(
            ["TXN1001", "DUPLICATE IN PROCESSED FILE"], issues
        )

    def test_unexpected_transaction(self):
        self.processed.append({
            "transaction_id": "TXN1002",
            "amount": "10.00",
            "status": "APPROVED"
        })
        issues = reconcile(self.expected, self.processed)
        self.assertIn(
            ["TXN1002", "UNEXPECTED TRANSACTION"], issues
        )

    def test_missing_required_field(self):
        self.expected[0].pop("expected_status")
        issues = reconcile(self.expected, self.processed)
        self.assertTrue(
            any("MISSING FIELD" in issue for _, issue in issues)
        )

    def test_invalid_amount(self):
        self.expected[0]["amount"] = "not-a-number"
        issues = reconcile(self.expected, self.processed)
        self.assertIn(
            ["TXN1001", "INVALID AMOUNT IN INPUT FILE"], issues
        )

    def test_duplicate_input_transaction(self):
        self.expected.append(self.expected[0].copy())
        issues = reconcile(self.expected, self.processed)
        self.assertIn(
            ["TXN1001", "DUPLICATE IN INPUT FILE"], issues
        )

    def test_batch_total_mismatch(self):
        self.processed[0]["amount"] = "30.00"
        issues = reconcile(self.expected, self.processed)
        self.assertTrue(
            any(
                txn_id == "BATCH" and "TOTAL MISMATCH" in issue
                for txn_id, issue in issues
            )
        )


if __name__ == "__main__":
    unittest.main()
