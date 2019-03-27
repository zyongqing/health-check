import logging
from health_check.result import Result


def evaluate_rules(source, rules, key=lambda x: x):
    for rule in rules:
        if rule.evaluate(source, key=key):
            return Result.create_result(source, rule)
    else:
        return Result(logging.INFO, source)


class Rule:
    def __init__(self, level, validator, desc="", rec=""):
        self.level = level
        self.validator = validator
        self.desc = desc
        self.rec = rec

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self.validator!r}, {self.desc!r}, {self.rec!r})"
        )

    def evaluate(self, source, key=lambda x: x):
        return self.validator(key(source))
