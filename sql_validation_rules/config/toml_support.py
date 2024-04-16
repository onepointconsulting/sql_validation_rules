from pathlib import Path
import tomli
from sql_validation_rules.config.config import cfg


def read_toml(file: Path) -> dict:
    with open(file, "rb") as f:
        return tomli.load(f)


def read_prompts_toml() -> dict:
    return read_toml(cfg.project_root / "prompts.toml")


prompts = read_prompts_toml()

if __name__ == "__main__":
    from sql_validation_rules.config.log_factory import logger

    assert prompts is not None
    assert prompts["sql_validation"] is not None
    logger.info("prompts: %s", prompts)
    logger.info("prompts: %s", prompts["sql_validation"]["main"]["human_message"])
