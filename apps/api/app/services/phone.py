import phonenumbers
from phonenumbers import NumberParseException
from phonenumbers.phonenumberutil import PhoneNumberFormat


DEFAULT_REGION = "IN"


def normalize_phone_number(phone_number: str) -> str:
    """
    Normalize a phone number to E.164 format.

    Example:
        9876543210 -> +919876543210
    """

    phone_number = phone_number.strip()

    try:
        parsed_number = phonenumbers.parse(
            phone_number,
            DEFAULT_REGION,
        )
    except NumberParseException as exc:
        raise ValueError("Invalid phone number.") from exc

    if not phonenumbers.is_valid_number(parsed_number):
        raise ValueError("Invalid phone number.")

    return phonenumbers.format_number(
        parsed_number,
        PhoneNumberFormat.E164,
    )

