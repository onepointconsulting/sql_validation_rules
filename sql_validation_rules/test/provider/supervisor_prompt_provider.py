def create_single_interaction():
    return """Please extract 2 SQL validation rules for column web_suite_number in table web_site."""


def create_until_repeat_web_suite_number():
    return """Please extract SQL validation rules for column web_suite_number in table web_site as long as new ones can be found. 
When you cannot find new ones stop"""


def create_until_makes_no_sense():
    return """Please extract SQL validation rules for column web_suite_number in table web_site as long as you can generate more meaningful rules. Stop when there are no more meaningful rules to generate on this field."""


def create_until_no_more_meaningful():
    return """Please extract SQL validation rules for column web_suite_number in table web_site 
as long as you can generate more meaningful rules. Stop when there are no more meaningful rules to generate on this field."""


def create_until_repeat_cc_tax_percentage():
    return """Please extract statistical SQL validation rules for column cc_tax_percentage in table call_center as long as new ones can be found. 
When you cannot find new ones stop"""


def create_until_repeat_cc_tax_percentage_no_type():
    return """Please extract SQL validation rules for column cc_tax_percentage in table call_center as long as new ones can be found. 
When you cannot find new ones stop. Make sure you find out details about the column before you choose which validator to take. 
If the type of the field is decimal you should use the statistical SQL validation"""
