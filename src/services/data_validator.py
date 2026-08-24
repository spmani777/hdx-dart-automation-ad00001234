"""DaRT Data Remediation & Banking Validation Logic."""

import re
from typing import Any


class DataValidator:
    """Enterprise Data Validator for Banking Records & Ledgers."""

    # Standard IBAN / Account Pattern
    ACCOUNT_REGEX = re.compile(r"^[A-Z0-9]{8,24}$")

    @classmethod
    def validate_account_number(cls, account_number: str) -> bool:
        """Validate format of banking account number."""
        if not account_number or not isinstance(account_number, str):
            return False
        return bool(cls.ACCOUNT_REGEX.match(account_number.strip().upper()))

    @classmethod
    def validate_transaction_amount(cls, amount: float | int) -> bool:
        """Verify transaction amount is a valid positive decimal within limit."""
        if not isinstance(amount, int | float):
            return False
        return 0 < amount <= 100_000_000.00

    @classmethod
    def remediate_record(cls, raw_record: dict[str, Any]) -> dict[str, Any]:
        """Sanitize, normalize and remediate raw transaction records."""
        account_raw = str(raw_record.get("account_id", "")).strip().upper()
        amount_raw = raw_record.get("amount", 0.0)

        try:
            amount = float(amount_raw)
        except (ValueError, TypeError):
            amount = 0.0

        currency = str(raw_record.get("currency", "USD")).strip().upper()
        if len(currency) != 3:
            currency = "USD"

        is_valid_account = cls.validate_account_number(account_raw)
        is_valid_amount = cls.validate_transaction_amount(amount)

        status = "REMEDIATED" if (is_valid_account and is_valid_amount) else "REJECTED"

        return {
            "record_id": raw_record.get("id", "UNKNOWN"),
            "account_id": account_raw,
            "amount": round(amount, 2),
            "currency": currency,
            "status": status,
            "remediation_applied": [
                "TRIM_WHITESPACE",
                "UPPERCASE_STANDARDIZATION",
                "CURRENCY_NORMALIZATION",
            ],
            "valid": status == "REMEDIATED",
        }