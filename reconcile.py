
from datetime import datetime
from pathlib import Path
import csv
from decimal import Decimal, InvalidOperation
from collections import Counter


def read_transactions(filename, required_columns):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"{filename} is empty or has no header.")

        missing_columns = set(required_columns) - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                f"{filename} is missing columns: {', '.join(sorted(missing_columns))}"
            )

        return list(reader)


def validate_rows(rows, required_fields, amount_field, source_name):
    valid_rows = []
    issues = []

    for row_number, row in enumerate(rows, start=2):
        txn_id = row.get("transaction_id", "").strip()
        label = txn_id if txn_id else f"ROW {row_number}"

        missing_fields = [
            field for field in required_fields
            if not str(row.get(field) or "").strip()
        ]

        if missing_fields:
            issues.append([
                label,
                f"MISSING FIELD IN {source_name}: {', '.join(missing_fields)}"
            ])
            continue

        try:
            amount = Decimal(row[amount_field])

            if not amount.is_finite():
                raise InvalidOperation

        except InvalidOperation:
            issues.append([
                label,
                f"INVALID AMOUNT IN {source_name}"
            ])
            continue

        valid_rows.append(row)

    return valid_rows, issues


def reconcile(expected, processed):
    issues = []

    # Validate both sets of transactions
    expected, expected_issues = validate_rows(
        expected,
        ["transaction_id", "amount", "expected_status"],
        "amount",
        "INPUT FILE"
    )

    processed, processed_issues = validate_rows(
        processed,
        ["transaction_id", "amount", "status"],
        "amount",
        "PROCESSED FILE"
    )

    issues.extend(expected_issues)
    issues.extend(processed_issues)

    # Count transaction IDs
    expected_counts = Counter(
        row["transaction_id"] for row in expected
    )

    processed_counts = Counter(
        row["transaction_id"] for row in processed
    )

    # Detect duplicates in both files
    for txn_id, count in expected_counts.items():
        if count > 1:
            issues.append([txn_id, "DUPLICATE IN INPUT FILE"])

    for txn_id, count in processed_counts.items():
        if count > 1:
            issues.append([txn_id, "DUPLICATE IN PROCESSED FILE"])

    # Calculate batch totals
    expected_total = sum(
        (Decimal(row["amount"]) for row in expected),
        Decimal("0")
    )

    processed_total = sum(
        (Decimal(row["amount"]) for row in processed),
        Decimal("0")
    )

    if expected_total != processed_total:
        issues.append([
            "BATCH",
            f"TOTAL MISMATCH: expected {expected_total:.2f}, "
            f"processed {processed_total:.2f}"
        ])

    # Create transaction lookup dictionaries
    expected_by_id = {
        row["transaction_id"]: row for row in expected
    }

    processed_by_id = {
        row["transaction_id"]: row for row in processed
    }

    # Compare expected transactions against processed transactions
    for txn_id, expected_row in expected_by_id.items():

        if txn_id not in processed_by_id:
            issues.append([txn_id, "MISSING TRANSACTION"])
            continue

        actual_row = processed_by_id[txn_id]

        if Decimal(expected_row["amount"]) != Decimal(actual_row["amount"]):
            issues.append([txn_id, "AMOUNT MISMATCH"])

        if expected_row["expected_status"] != actual_row["status"]:
            issues.append([txn_id, "STATUS MISMATCH"])

    # Detect unexpected transactions
    for txn_id in processed_by_id:
        if txn_id not in expected_by_id:
            issues.append([txn_id, "UNEXPECTED TRANSACTION"])

    return issues



def main():
    try:
        expected = read_transactions(
            "input_transactions.csv",
            ["transaction_id", "amount", "expected_status"]
        )

        processed = read_transactions(
            "processed_transactions.csv",
            ["transaction_id", "amount", "status"]
        )

    except (FileNotFoundError, ValueError) as error:
        print(f"INPUT ERROR: {error}")
        return

    issues = reconcile(expected, processed)

    # Calculate batch statistics
    expected_count = len(expected)
    processed_count = len(processed)

    def calculate_total(rows):
        total = Decimal("0")

        for row in rows:
            try:
                amount = Decimal(row["amount"])
                if amount.is_finite():
                    total += amount
            except (InvalidOperation, KeyError):
                continue

        return total

    expected_total = calculate_total(expected)
    processed_total = calculate_total(processed)

    # Determine overall result
    result = "PASS" if not issues else "FAIL"

    # Capture execution time
    run_time = datetime.now().astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )

    # Display summary
    print("\nTRANSACTION RECONCILIATION REPORT")
    print("=================================")

    print(f"Execution time:       {run_time}")
    print(f"Overall result:       {result}")

    print("\nBATCH STATISTICS")
    print("----------------")
    print(f"Expected transactions:  {expected_count}")
    print(f"Processed transactions: {processed_count}")
    print(f"Expected batch total:   {expected_total:.2f}")
    print(f"Processed batch total:  {processed_total:.2f}")
    print(f"Discrepancies found:    {len(issues)}")

    print("\nDETAILED FINDINGS")
    print("-----------------")

    if not issues:
        print("No discrepancies found.")
    else:
        for txn_id, issue in issues:
            print(f"{txn_id}: {issue}")

    # Export detailed report
    report_name = "reconciliation_report.csv"

    with open(
        report_name,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "transaction_id",
            "issue",
            "execution_time",
            "overall_result"
        ])

        for txn_id, issue in issues:
            writer.writerow([
                txn_id,
                issue,
                run_time,
                result
            ])

    print(f"\nDetailed report saved: {report_name}")


if __name__ == "__main__":
    main()
