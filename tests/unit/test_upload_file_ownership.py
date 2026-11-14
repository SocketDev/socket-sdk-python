import io
from unittest.mock import Mock

import pytest

from socketdev.report import Report


@pytest.mark.parametrize("request_fails", [False, True])
def test_report_upload_closes_files_opened_from_paths(tmp_path, request_fails):
    path = tmp_path / "package.json"
    path.write_text("{}")
    api = Mock()
    uploaded = []

    def request(**kwargs):
        stream = kwargs["files"][0][1][1]
        uploaded.append(stream)
        assert not stream.closed
        assert stream.read() == b"{}"
        if request_fails:
            raise RuntimeError("request failed")
        return Mock(status_code=200, json=lambda: {"id": "report"})

    api.do_request.side_effect = request
    if request_fails:
        with pytest.raises(RuntimeError, match="request failed"):
            Report(api).create([("package", str(path))])
    else:
        assert Report(api).create([("package", str(path))]) == {"id": "report"}
    assert uploaded[0].closed


def test_report_upload_leaves_caller_owned_stream_open():
    api = Mock()
    api.do_request.return_value.status_code = 200
    stream = io.BytesIO(b"{}")
    Report(api).create([("package", ("package.json", stream))])
    assert not stream.closed
