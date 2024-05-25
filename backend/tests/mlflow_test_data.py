def remove_attributes(model, attributes):
    return {key: value for key, value in model.items() if key not in attributes}


# MLflow Schema
attributes_to_remove = [
    "run_id",
    "run_link",
    "last_updated_timestamp",
    "status",
    "current_stage",
]

common_data = {
    "churn_model": {
        "creation_timestamp": 1715438791345,
        "description": "Model to predict customer churn, currently in evaluation.",
        "source": "mlflow-artifacts:/881970382704382419/764238746b7f4e7397a706a1f59a4016/artifacts/model",
        "tags": [
            {"key": "stage", "value": "evaluation"},
            {"key": "approved", "value": "false"},
        ],
        "last_updated_timestamp": None,
        "run_id": None,
        "status": "READY",
        "run_link": "",
        "current_stage": "None",
    },
    "uplift_model": {
        "creation_timestamp": 1715244800000,
        "description": "Uplift model used for predicting customer conversion probabilities.",
        "source": "mlflow-artifacts:/916798459276195935/71153ac3ca0441a59556b061d24d1705/artifacts/uplift_model",
        "tags": [
            {"key": "stage", "value": "production"},
            {"key": "approved", "value": "true"},
        ],
        "last_updated_timestamp": None,
        "run_id": None,
        "status": "READY",
        "run_link": "",
        "current_stage": "None",
    },
}

registered_models = {
    "registered_models": [
        {
            "name": "churn_model",
            "creation_timestamp": common_data["churn_model"]["creation_timestamp"],
            "last_updated_timestamp": common_data["churn_model"][
                "last_updated_timestamp"
            ],
            "latest_versions": [
                {**common_data["churn_model"], "name": "churn_model", "version": "1"},
                {**common_data["churn_model"], "name": "churn_model", "version": "2"},
            ],
        },
        {
            "name": "uplift_model",
            "creation_timestamp": common_data["uplift_model"]["creation_timestamp"],
            "last_updated_timestamp": common_data["uplift_model"][
                "last_updated_timestamp"
            ],
            "latest_versions": [
                {**common_data["uplift_model"], "name": "uplift_model", "version": "1"}
            ],
        },
    ]
}

latest_model_version = {
    "model_versions": [
        {**common_data["churn_model"], "name": "churn_model", "version": "2"}
    ]
}

model_versions = {
    "model_versions": [
        {**common_data["churn_model"], "name": "churn_model", "version": "1"},
        {**common_data["churn_model"], "name": "churn_model", "version": "2"},
        {**common_data["uplift_model"], "name": "uplift_model", "version": "1"},
    ]
}

model_version = {
    "model_version": {
        **common_data["churn_model"],
        "name": "churn_model",
        "version": "2",
    }
}


models_with_type = [
    {
        **remove_attributes(common_data["churn_model"], attributes_to_remove),
        "name": "churn_model",
        "version": "1",
        "type": "MLflow",
    },
    {
        **remove_attributes(common_data["churn_model"], attributes_to_remove),
        "name": "churn_model",
        "version": "2",
        "type": "MLflow",
    },
    {
        **remove_attributes(common_data["uplift_model"], attributes_to_remove),
        "name": "uplift_model",
        "version": "1",
        "type": "MLflow",
    },
]

models_without_type = [
    {
        **remove_attributes(common_data["churn_model"], attributes_to_remove),
        "name": "churn_model",
        "version": "1",
    },
    {
        **remove_attributes(common_data["churn_model"], attributes_to_remove),
        "name": "churn_model",
        "version": "2",
    },
    {
        **remove_attributes(common_data["uplift_model"], attributes_to_remove),
        "name": "uplift_model",
        "version": "1",
    },
]
