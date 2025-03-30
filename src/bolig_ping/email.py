"""Sending emails with flat listings."""

import yagmail
from dotenv import load_dotenv

from .data_models import Flat

load_dotenv()


def compose_email(flats: list[Flat]) -> tuple[str, str]:
    """Compose an email with the given flats.

    Args:
        flats:
            The flats to compose the email with.

    Returns:
        A pair (subject, contents) for the email.
    """
    match len(flats):
        case 0:
            raise ValueError("Cannot compose an email with no flats.")
        case 1:
            subject = "[BoligPing] Found a new flat!"
            contents = "Hi,\n\nI found a new flat that you might be interested in:\n\n"
        case _:
            subject = f"[BoligPing] Found {len(flats)} new flats!"
            contents = (
                "Hi,\n\nI found some new flats that you might be interested in:\n\n"
            )
    contents += "\n\n".join(flat.to_html() for flat in flats)
    contents += "\n\nHave a splendid day!\n\nBest regards,\nBoligPing"
    return subject, contents


def send_email(
    from_email: str, password: str, to_email: str, subject: str, contents: str
) -> None:
    """Send an email with the given contents.

    Args:
        from_email:
            The email to send the email from.
        password:
            The password for the from email.
        to_email:
            The email to send the email to.
        subject:
            The subject of the email.
        contents:
            The contents of the email.
    """
    yagmail.SMTP(user=from_email, password=password).send(
        to=to_email, subject=subject, contents=contents
    )
