import unittest
from unittest import TestCase

from sql_validation_rules.agent.prompt_factory import create_sql_validation_template


class TestPromptFactory(TestCase):
    def test_prompt(self):
        prompt_template = create_sql_validation_template()
        assert prompt_template is not None


if __name__ == "__main__":
    unittest.main()
