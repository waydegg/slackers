from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

import pytest

from slackers.hooks import commands


@pytest.mark.usefixtures("pass_header_verification")
def post_commands_should_emit_commands_event_with_payload(mocker, client: TestClient):
    @commands.on("foo")
    def on_foo(payload):
        inspection(payload=payload)

    inspection = mocker.Mock()
    headers = {"X-Slack-Request-Timestamp": "123", "X-Slack-Signature": "FAKE_SIG"}
    command = {
        "token": "SLACK_TOKEN",
        "user_id": "USER_ID",
        "command": "/foo",
        "response_url": "https://example.com/response_url",
        "trigger_id": "TRIGGER_ID",
        "user_id": "USER_ID",
        "user_name": "USER_NAME",
        "team_id": "TEAM_ID",
        "channel_id": "CHANNEL_ID",
    }

    response = client.post(url="/commands", data=command, headers=headers)

    assert HTTP_200_OK == response.status_code
    inspection.assert_called_once_with(payload=command)
