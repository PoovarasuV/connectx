import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.phone_otp import PhoneOTP


OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 5


def generate_otp() -> str:
    """Generate a cryptographically secure 6-digit OTP."""

    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(otp: str) -> str:
    """Hash an OTP before storing it in the database."""

    return bcrypt.hashpw(
        otp.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_otp(otp: str, otp_hash: str) -> bool:
    """Verify an OTP against its stored hash."""

    return bcrypt.checkpw(
        otp.encode("utf-8"),
        otp_hash.encode("utf-8"),
    )


def create_otp(
    db: Session,
    phone_number: str,
) -> str:
    """Generate and store a new OTP."""

    otp = generate_otp()

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=OTP_EXPIRY_MINUTES
    )

    otp_record = PhoneOTP(
        phone_number=phone_number,
        otp_hash=hash_otp(otp),
        expires_at=expires_at,
        attempts=0,
        max_attempts=MAX_OTP_ATTEMPTS,
        is_used=False,
    )

    db.add(otp_record)
    db.commit()

    return otp


def verify_otp_for_phone(
    db: Session,
    phone_number: str,
    otp: str,
) -> bool:
    """Verify the latest unused OTP for a phone number."""

    otp_record = db.scalar(
        select(PhoneOTP)
        .where(
            PhoneOTP.phone_number == phone_number,
            PhoneOTP.is_used.is_(False),
        )
        .order_by(PhoneOTP.created_at.desc())
    )

    if otp_record is None:
        return False

    now = datetime.now(timezone.utc)

    if now >= otp_record.expires_at:
        return False

    if otp_record.attempts >= otp_record.max_attempts:
        return False

    otp_record.attempts += 1

    if not verify_otp(otp, otp_record.otp_hash):
        db.commit()
        return False

    otp_record.is_used = True
    db.commit()

    return True
