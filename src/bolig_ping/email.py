"""Sending emails with flat listings."""

import os

import yagmail
from dotenv import load_dotenv

from .data_models import Flat

load_dotenv()


def send_flats(to_email: str, flats: list[Flat]) -> None:
    """Send an email with the found flats.

    Args:
        to_email:
            The email to send the email to.
        flats:
            The flats to send in the email.
    """
    match len(flats):
        case 0:
            return
        case 1:
            subject = "[BoligPing] Found a new flat!"
        case _:
            subject = f"[BoligPing] Found {len(flats)} new flats!"

    contents = "Hi,\n\nI found some new flats that you might be interested in:\n\n"
    contents += "\n\n".join(flat.to_html() for flat in flats)
    contents += "\n\nHave a splendid day!\n\nBest regards,\nBoligPing"

    send_email(
        from_email=os.environ["GMAIL_EMAIL"],
        password=os.environ["GMAIL_PASSWORD"],
        to_email=to_email,
        subject=subject,
        contents=contents,
    )


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
