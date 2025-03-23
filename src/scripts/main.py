"""Main script.

Usage:
    uv run src/scripts/main.py <config_key>=<config_value> ...
"""

import hydra
from omegaconf import DictConfig
from bolig_ping.module import example_function


@hydra.main(config_path="../../config", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function.

    Args:
        config:
            The Hydra config for your project.
    """
    example_function(config=config)


if __name__ == "__main__":
    main()
