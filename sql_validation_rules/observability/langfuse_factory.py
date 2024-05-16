from langfuse.callback import CallbackHandler

from sql_validation_rules.config.config import cfg


def create_langfuse_handler():
    return CallbackHandler(
        public_key=cfg.langfuse_config.langfuse_public_key,
        secret_key=cfg.langfuse_config.langfuse_secret_key,
        host=cfg.langfuse_config.langfuse_host,
    )
