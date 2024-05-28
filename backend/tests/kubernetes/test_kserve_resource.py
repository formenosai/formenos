from app.kubernetes.kserve_resource import InferenceServiceResource


def test_inference_service_resource():
    name = "test-service"
    service_account = "default"
    storage_uri = "s3://bucket/model"
    instance_type = "ml.cpu.small"
    model_format = "mlflow"
    batcher = True
    timeout = 120
    max_batch_size = 64
    max_latency = 1000
    autoscaling = True
    min_replicas = 2
    max_replicas = 5
    logger = True
    mode = "all"
    url = "http://logger"
    prometheus = True
    port = "9090"
    path = "/metrics"
    runtime = "kserve-mlserver"

    resource = InferenceServiceResource(
        name=name,
        service_account=service_account,
        storage_uri=storage_uri,
        instance_type=instance_type,
        model_format=model_format,
        batcher=batcher,
        timeout=timeout,
        max_batch_size=max_batch_size,
        max_latency=max_latency,
        autoscaling=autoscaling,
        min_replicas=min_replicas,
        max_replicas=max_replicas,
        logger=logger,
        mode=mode,
        url=url,
        prometheus=prometheus,
        port=port,
        path=path,
        runtime=runtime,
    )

    expected_spec = {
        "predictor": {
            "model": {
                "modelFormat": {"name": model_format},
                "runtime": runtime,
                "storageUri": storage_uri,
                "resources": {
                    "requests": {"cpu": "1", "memory": "2Gi"},
                    "limits": {"cpu": "1", "memory": "2Gi"},
                },
            },
            "serviceAccountName": service_account,
            "batcher": {
                "timeout": timeout,
                "maxBatchSize": max_batch_size,
                "maxLatency": max_latency,
            },
            "logger": {"mode": mode, "url": url},
            "minReplicas": min_replicas,
            "maxReplicas": max_replicas,
        },
        "annotations": {
            "prometheus.kserve.io/port": port,
            "prometheus.kserve.io/path": path,
        },
    }

    expected_metadata = {
        "name": name,
        "annotations": {"serving.kserve.io/enable-prometheus-scraping": "true"},
    }

    assert resource.spec == expected_spec
    assert resource.metadata == expected_metadata
    assert resource.spec["annotations"] == expected_spec["annotations"]


def test_to_dict():
    name = "test-service"
    service_account = "default"
    storage_uri = "s3://bucket/model"
    instance_type = "ml.cpu.small"

    resource = InferenceServiceResource(
        name=name,
        service_account=service_account,
        storage_uri=storage_uri,
        instance_type=instance_type,
    )

    expected_dict = {
        "apiVersion": "serving.kserve.io/v1beta1",
        "kind": "InferenceService",
        "metadata": {"name": name, "annotations": {}},
        "spec": {
            "predictor": {
                "model": {
                    "modelFormat": {"name": "mlflow"},
                    "runtime": "kserve-mlserver",
                    "storageUri": storage_uri,
                    "resources": {
                        "requests": {"cpu": "1", "memory": "2Gi"},
                        "limits": {"cpu": "1", "memory": "2Gi"},
                    },
                },
                "serviceAccountName": service_account,
            }
        },
    }

    assert resource.to_dict() == expected_dict
