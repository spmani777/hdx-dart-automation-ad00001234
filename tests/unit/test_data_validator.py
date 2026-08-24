"""Unit tests for DataValidator service."""

import pytest
from src.services.data_validator import DataValidator


def test_validate_account_number_valid():
    """Test valid banking account formats."""
    assert DataValidator.validate_account_number("ACC12345678") is True
    assert DataValidator.validate_account_number("GB29NWBK60161331926819") is True
    assert DataValidator.validate_account_number("  acc99887766  ") is True


def test_validate_account_number_invalid():
    """Test invalid banking account formats."""
    assert DataValidator.validate_account_number("SHORT") is False
    assert DataValidator.validate_account_number("ACC-INVALID#123") is False
    assert DataValidator.validate_account_number("") is False
    assert DataValidator.validate_account_number(None) is False


def test_validate_transaction_amount():
    """Test transaction amount boundary validations."""
    assert DataValidator.validate_transaction_amount(100.50) is True
    assert DataValidator.validate_transaction_amount(1) is True
    assert DataValidator.validate_transaction_amount(100_000_000.00) is True
    assert DataValidator.validate_transaction_amount(0) is False
    assert DataValidator.validate_transaction_amount(-50.0) is False
    assert DataValidator.validate_transaction_amount(100_000_001.00) is False
    assert DataValidator.validate_transaction_amount("not-a-number") is False


def test_remediate_record_success():
    """Test successful remediation of raw dirty record."""
    raw = {
        "id": "REC-101",
        "account_id": " acc12345678 ",
        "amount": "250.75",
        "currency": "usd ",
    }
    result = DataValidator.remediate_record(raw)
    assert result["status"] == "REMEDIATED"
    assert result["valid"] is True
    assert result["account_id"] == "ACC12345678"
    assert result["amount"] == 250.75
    assert result["currency"] == "USD"


def test_remediate_record_failure():
    """Test remediation rejection for invalid account and negative amount."""
    raw = {
        "id": "REC-999",
        "account_id": "BAD",
        "amount": -50.0,
        "currency": "EUR",
    }
    result = DataValidator.remediate_record(raw)
    assert result["status"] == "REJECTED"
    assert result["valid"] is False

