import functools

# add project base path into sys.path
# when run in script mode
if __package__ == "":
    from pathlib import Path
    import sys

    current_path = Path(__file__).resolve()
    # health_check/health_check/os/linux
    #    ^
    #    └─────────────────────────[3]
    lib_base = current_path.parents[3]
    sys.path.append(str(lib_base))

from health_check.pipe import strip_line
from health_check.os.windows.connection import LINE_END

strip_line = functools.partial(strip_line, end=LINE_END)
