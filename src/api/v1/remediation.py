"""DaRT Remediation Endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.services.audit_trail import AuditTrail
from src.services.data_validator import DataValidator

router = APIRouter(prefix="/remediation", tags=["Data Remediation Engine"])


class TransactionRecord(BaseModel):
    """Raw transaction record payload."""

    id: str = Field(..., description="Record identifier")
    account_id: str = Field(..., description="Banking account number (alphanumeric, 8-24 chars)")
    amount: float = Field(..., description="Transaction amount (positive, max 100M)")
    currency: str = Field(default="USD", description="ISO 4217 currency code")


class BatchRemediationRequest(BaseModel):
    """Batch payload for transaction remediation."""

    batch_id: str = Field(..., description="Unique batch identifier")
    records: list[TransactionRecord]


@router.post("/process", status_code=status.HTTP_200_OK)
def process_single_record(record: TransactionRecord) -> dict[str, Any]:
    """Validate and remediate an individual transaction record."""
    remediated = DataValidator.remediate_record(record.model_dump())
    audit_event = AuditTrail.create_event(
        event_type="SINGLE_RECORD_REMEDIATION",
        details={"record_id": record.id, "status": remediated["status"]},
    )
    return {
        "result": remediated,
        "audit": audit_event,
    }


@router.post("/batch", status_code=status.HTTP_200_OK)
def process_batch(payload: BatchRemediationRequest) -> dict[str, Any]:
    """Process and remediate a batch of records."""
    if not payload.records:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch must contain at least one record.",
        )

    results = [DataValidator.remediate_record(r.model_dump()) for r in payload.records]
    valid_count = sum(1 for r in results if r["valid"])

    audit_event = AuditTrail.create_event(
        event_type="BATCH_REMEDIATION_PROCESSED",
        details={
            "batch_id": payload.batch_id,
            "total_records": len(payload.records),
            "remediated_records": valid_count,
        },
    )

    return {
        "batch_id": payload.batch_id,
        "total": len(payload.records),
        "remediated_count": valid_count,
        "results": results,
        "audit": audit_event,
    }