from typing import Any
import sys

def decorate_namespace(req: Any) -> dict[str,Any]:
    print("Req:", req, file=sys.stderr)
    return {}
