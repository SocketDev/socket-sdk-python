import json
from unittest.mock import Mock

from socketdev.repos import Repos


def test_repository_update_serializes_keyword_arguments():
    api = Mock()
    api.do_request.return_value.status_code = 200
    api.do_request.return_value.json.return_value = {"name": "widgets"}

    assert Repos(api).update("example", "widgets", description="updated", defaultBranch="main") == {"name": "widgets"}
    assert json.loads(api.do_request.call_args.kwargs["payload"]) == {
        "description": "updated",
        "defaultBranch": "main",
    }
