import logging


def setup_logging() -> None:
    """Configure the root logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],  # Directs logs to stdout, visible in CloudWatch
        force=True,
    )
