FROM python:3.11-slim-bookworm

# Install uv
RUN sudo apt-get update && sudo apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    source $HOME/.cargo/env

# Move the files into the container
WORKDIR /project
COPY . /project

# Install dependencies
RUN uv sync --no-dev --no-cache

# Run the script
CMD uv run python src/scripts/main.py
