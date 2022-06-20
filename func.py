from typing import Any
from flask import Request
import json
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

def sa_binding(namespace: str, role: str) -> dict[str, Any]:
    return {"apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "RoleBinding",
            "metadata": {
                "name": "default-permit-" + role,
                "namespace": namespace,
            },
            "roleRef": {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "ClusterRole",
                "name": role,
            },
            "subjects": [
                {"kind": "ServiceAccount",
                 "name": "default",
                },
            ],
           }

def decorate_namespace(req: Request) -> str: # dict[str,Any]:
    """Implementation the 'sync' metacontroller API.

    See https://metacontroller.github.io/metacontroller/api/decoratorcontroller.html#sync-hook-request
    for details.
    """
    data = req.get_json()
    print("Req:", data, file=sys.stderr)
    ns = data["object"]["metadata"]["name"]
    resp = json.dumps(dict(labels=dict(),
                annotations=dict(),
                status=None,
                attachments=[reg_creds(ns), sa(ns), sa_binding(ns, "deliverable"), sa_binding(ns, "workload")],
               ))
    print("Resp:", resp, file=sys.stderr)
    return resp
                
