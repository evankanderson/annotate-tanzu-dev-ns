from typing import Any
from flask import Request
import sys

def reg_creds(namespace: str) -> dict[str, Any]:
    return {"apiVersion": "v1",
            "kind": "Secret",
            "metadata": {
                "name": "tap-registry",
                "namespace": namespace,
                "annotations": {
                    "secretgen.carvel.dev/image-pull-secret": "",
                },
            },
            "type": "kubernetes.io/dockerconfigjson",
            "data": {
                ".dockerconfigjson": "e30K",
            },
           }

def sa(namespace: str) -> dict[str, Any]:
    return {"apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "name": "default",
                "namespace": namespace,
            },
            "secrets": [
                {"name": "registry-credentials"},
            ],
            "imagePullSecrets": [
                {"name": "registry-credentials"},
                {"name": "tap-registry"},
            ],
           }

def decorate_namespace(req: Request) -> dict[str,Any]:
    data = req.get_json()
    print("Req:", data, file=sys.stderr)
    ns = data["object"]["metadata"]["name"]
    return dict(labels={},
                annotations={},
                status=None,
                attachments=[reg_creds(ns),sa(ns)],
               )
                
