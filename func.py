from typing import Any
from flask import Request
import sys

def decorate_namespace(req: Request) -> dict[str,Any]:
    data = req.get_json()
    print("Req:", data, file=sys.stderr)
    return {}
