from typing import Dict, Optional

from app.core.config import settings
from app.kubernetes.base_resource import BaseResource


class InferenceServiceResource(BaseResource):
    API_VERSION: str = "serving.kserve.io/v1beta1"
    KIND: str = "InferenceService"

    def __init__(
        self,
        name: str,
        service_account: str,
        storage_uri: str,
        instance_type: str,
        model_format: str = "mlflow",
        batcher: bool = False,
        timeout: int = 60,
        max_batch_size: int = 32,
        max_latency: int = 500,
        autoscaling: bool = False,
        min_replicas: int = 1,
        max_replicas: int = 1,
        logger: bool = False,
        mode: str = "all",
        url: Optional[str] = None,
        prometheus: bool = False,
        port: str = "8082",
        path: str = "/metrics",
        runtime: str = "kserve-mlserver",
    ) -> None:
        self.api_version = self.API_VERSION
        self.kind = self.KIND
        self.metadata: Dict[str, Dict[str, str]] = {"name": name, "annotations": {}}
        self.spec: Dict[str, Dict[str, Dict[str, str]]] = {"predictor": {"model": {}}}

        self.spec["predictor"].update(
            {
                "model": {
                    "modelFormat": {"name": model_format},
                    "runtime": runtime,
                    "storageUri": storage_uri,
                },
                "serviceAccountName": service_account,
            }
        )

        cpu = settings.INSTANCE_TYPES[instance_type]["cpu"]
        memory = settings.INSTANCE_TYPES[instance_type]["memory"]
        resources = {
            "requests": {"cpu": cpu, "memory": memory},
            "limits": {"cpu": cpu, "memory": memory},
        }
        self.spec["predictor"]["model"].update({"resources": resources})

        if batcher:
            self.spec["predictor"].update(
                {
                    "batcher": {
                        "timeout": timeout,
                        "maxBatchSize": max_batch_size,
                        "maxLatency": max_latency,
                    }
                }
            )

        if logger:
            self.spec["predictor"].update({"logger": {"mode": mode, "url": url}})

        if autoscaling:
            self.spec["predictor"].update(
                {"minReplicas": min_replicas, "maxReplicas": max_replicas}
            )

        if prometheus:
            self.metadata["annotations"].update(
                {"serving.kserve.io/enable-prometheus-scraping": "true"}
            )
            self.spec.setdefault("annotations", {}).update(
                {"prometheus.kserve.io/port": port, "prometheus.kserve.io/path": path}
            )

    def to_dict(self) -> Dict[str, Dict]:
        return {
            "apiVersion": self.api_version,
            "kind": self.kind,
            "metadata": self.metadata,
            "spec": self.spec,
        }
