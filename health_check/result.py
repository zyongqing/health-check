class Result:
    def __init__(self, level, source, rec=""):
        self.level = level
        self.source = source
        self.rec = rec

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self.level!r}, {self.source!r}, {self.rec!r})"
        )

    def __eq__(self, value):
        return (
            self.level == value.level
            and self.source == value.source
            and self.rec == value.rec
        )

    @classmethod
    def create_result(cls, source, rule):
        return Result(rule.level, source, rule.rec)
