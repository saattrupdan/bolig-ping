"""Checks related to the .env file in the repository.

Usage:
    uv run src/scripts/fix_dot_env_file.py [--non-interactive]
"""

from pathlib import Path

import click

# List of all the environment variables that are desired
DESIRED_ENVIRONMENT_VARIABLES = dict(
    GIT_NAME="Enter your full name, to be shown in Git commits:\n> ",
    GIT_EMAIL="Enter your email, as registered on your Github account:\n> ",
)


@click.command()
@click.option(
    "--non-interactive",
    is_flag=True,
    default=False,
    help="If set, the script will not ask for user input.",
)
def fix_dot_env_file(non_interactive: bool) -> None:
    """Ensures that the .env file exists and contains all desired variables.

    Args:
        non_interactive:
            If set, the script will not ask for user input.
    """
    env_path = Path(".env")
    name_and_email_path = Path(".name_and_email")

    # Ensure that the files exists
    env_path.touch(exist_ok=True)
    name_and_email_path.touch(exist_ok=True)

    # Extract all the lines in the files
    env_file_lines = [
        line for line in env_path.read_text().splitlines(keepends=False) if line.strip()
    ]
    name_and_email_file_lines = name_and_email_path.read_text().splitlines(
        keepends=False
    )

    # Extract all the environment variables in the files
    env_vars = {line.split("=")[0]: line.split("=")[1] for line in env_file_lines}
    name_and_email_vars = {
        line.split("=")[0]: line.split("=")[1] for line in name_and_email_file_lines
    }

    desired_env_vars = DESIRED_ENVIRONMENT_VARIABLES

    # For each of the desired environment variables, check if it exists in the .env
    # file
    env_vars_missing = [
        env_var for env_var in desired_env_vars.keys() if env_var not in env_vars
    ]

    # Create all the missing environment variables
    with env_path.open("a") as f:
        for env_var in env_vars_missing:
            value = ""

            if env_var in name_and_email_vars:
                value = name_and_email_vars[env_var]

            if value == "" and not non_interactive:
                value = input(desired_env_vars[env_var])

            f.write(f"{env_var}={value}\n")

    # Remove the name and email file
    name_and_email_path.unlink()


if __name__ == "__main__":
    fix_dot_env_file()
