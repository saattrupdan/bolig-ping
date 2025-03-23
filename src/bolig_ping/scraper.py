"""An example module for your project."""

import logging

from omegaconf import DictConfig

logger = logging.getLogger(__name__)


def example_function(config: DictConfig) -> None:
    """An example function for your project.

    Args:
        config:
            The Hydra config for your project.
    """
    logger.info("Hello World!")
    logger.info(f"Your config is: {config}")
