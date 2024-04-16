import unittest
from unittest import TestCase

from sql_validation_rules.config.config import cfg
from sql_validation_rules.config.toml_support import prompts


class TestTomlSupport(TestCase):
    def test_prompts(self):
        main_prompts = prompts["sql_validation"]["main"]
        assert main_prompts is not None


if __name__ == "__main__":
    unittest.main()
