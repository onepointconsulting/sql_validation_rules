import unittest
from unittest import TestCase

from sql_validation_rules.config.config import cfg


class TestConfig(TestCase):
    def test_config(self):
        assert cfg is not None
        assert cfg.llm is not None
        assert cfg.snowflake_config is not None
        assert cfg.project_root.exists()


if __name__ == "__main__":
    unittest.main()
