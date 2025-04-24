"""Sending emails with home listings."""

import yagmail

from .data_models import Home


def compose_email(homes: list[Home]) -> tuple[str, str]:
    """Compose an email with the given homes.

    Args:
        homes:
            The homes to compose the email with.

    Returns:
        A pair (subject, contents) for the email.
    """
    match len(homes):
        case 0:
            raise ValueError("Cannot compose an email with no homes.")
        case 1:
            subject = "[BoligPing] Found a new home!"
            contents = "Hi,\n\nI found a new home that you might be interested in:\n\n"
        case _:
            subject = f"[BoligPing] Found {len(homes)} new homes!"
            contents = (
                "Hi,\n\nI found some new homes that you might be interested in:\n\n"
            )
    contents += "\n\n".join(home.to_html() for home in homes)
    contents += "\n\nHave a splendid day!\n\nBest regards,\nBoligPing"
    return subject, contents


def send_emails(
    from_email: str, password: str, to_emails: list[str], subject: str, contents: str
) -> None:
    """Send an email with the given contents.

    Args:
        from_email:
            The email to send the email from.
        password:
            The password for the from email.
        to_emails:
            The emails to send the email to.
        subject:
            The subject of the email.
        contents:
            The contents of the email.
    """
    for to_email in to_emails:
        yagmail.SMTP(user=from_email, password=password).send(
            to=to_email, subject=subject, contents=contents
        )
