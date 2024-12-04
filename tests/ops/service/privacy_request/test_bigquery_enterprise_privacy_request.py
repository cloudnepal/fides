import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Set
from unittest import mock
from unittest.mock import ANY, Mock, call
from uuid import uuid4

import pydash
import pytest

from fides.api.models.audit_log import AuditLog, AuditLogAction
from fides.api.models.privacy_request import (
    ActionType,
    CheckpointActionRequired,
    ExecutionLog,
    ExecutionLogStatus,
    PolicyPreWebhook,
    PrivacyRequest,
    PrivacyRequestStatus,
)
from fides.api.schemas.masking.masking_configuration import MaskingConfiguration
from fides.api.schemas.masking.masking_secrets import MaskingSecretCache
from fides.api.schemas.policy import Rule
from fides.api.service.masking.strategy.masking_strategy import MaskingStrategy
from tests.ops.service.privacy_request.test_request_runner_service import (
    get_privacy_request_results,
)

PRIVACY_REQUEST_TASK_TIMEOUT = 5
# External services take much longer to return
PRIVACY_REQUEST_TASK_TIMEOUT_EXTERNAL = 60


@pytest.mark.integration_bigquery
@pytest.mark.integration_external
@pytest.mark.parametrize(
    "dsr_version",
    ["use_dsr_3_0", "use_dsr_2_0"],
)
@mock.patch("fides.api.models.privacy_request.PrivacyRequest.trigger_policy_webhook")
def test_create_and_process_access_request_bigquery_enterprise(
    trigger_webhook_mock,
    bigquery_enterprise_test_dataset_config,
    db,
    cache,
    policy,
    dsr_version,
    request,
    policy_pre_execution_webhooks,
    policy_post_execution_webhooks,
    run_privacy_request_task,
):
    request.getfixturevalue(dsr_version)  # REQUIRED to test both DSR 3.0 and 2.0

    customer_email = "customer-1@example.com"
    user_id = (
        1754  # this is a real (not generated) user id in the Stackoverflow dataset
    )
    data = {
        "requested_at": "2024-08-30T16:09:37.359Z",
        "policy_key": policy.key,
        "identity": {
            "email": customer_email,
            "stackoverflow_user_id": {
                "label": "Stackoverflow User Id",
                "value": user_id,
            },
        },
    }

    pr = get_privacy_request_results(
        db,
        policy,
        run_privacy_request_task,
        data,
        PRIVACY_REQUEST_TASK_TIMEOUT_EXTERNAL,
    )

    results = pr.get_raw_access_results()
    assert len(results.keys()) == 4

    for key in results.keys():
        assert results[key] is not None
        assert results[key] != {}

    users = results["enterprise_dsr_testing:users"]
    assert len(users) == 1
    user_details = users[0]
    assert user_details["id"] == user_id

    assert (
        len(
            [
                comment["user_id"]
                for comment in results["enterprise_dsr_testing:comments"]
            ]
        )
        == 16
    )
    assert (
        len(
            [post["user_id"] for post in results["enterprise_dsr_testing:post_history"]]
        )
        == 60
    )
    assert (
        len(
            [
                post["title"]
                for post in results["enterprise_dsr_testing:stackoverflow_posts"]
            ]
        )
        == 30
    )

    log_id = pr.execution_logs[0].id
    pr_id = pr.id

    finished_audit_log: AuditLog = AuditLog.filter(
        db=db,
        conditions=(
            (AuditLog.privacy_request_id == pr_id)
            & (AuditLog.action == AuditLogAction.finished)
        ),
    ).first()

    assert finished_audit_log is not None

    # Both pre-execution webhooks and both post-execution webhooks were called
    assert trigger_webhook_mock.call_count == 4

    for webhook in policy_pre_execution_webhooks:
        webhook.delete(db=db)

    for webhook in policy_post_execution_webhooks:
        webhook.delete(db=db)

    policy.delete(db=db)
    pr.delete(db=db)
    assert not pr in db  # Check that `pr` has been expunged from the session
    assert ExecutionLog.get(db, object_id=log_id).privacy_request_id == pr_id