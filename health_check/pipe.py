import functools


def filter_line(source, rule=lambda x: True):
    for line in source:
        if rule(line):
            yield line


skip_empty_line = functools.partial(filter_line, rule=lambda line: line)


def strip_line(source, end=""):
    for line in source:
        yield line.strip(end)


def skip_head_line(source, skips=1):
    for line_no, line in enumerate(source):
        if line_no >= skips:
            yield line
