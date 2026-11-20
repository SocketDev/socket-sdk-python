"""Multipart key collisions must fail before files are read or requests are sent."""

from collections import UserDict
from io import BytesIO
from unittest.mock import Mock, patch

import pytest
from requests import Request
from urllib3.fields import RequestField

from socketdev.fullscans import FullScans, FullScanParams
from socketdev.uploadmanifests import UploadManifests
from socketdev.utils import Utils


COLLISIONS = [
    (["./services/a/package.json"] * 2, {"base_paths": ["."]}, "services/a/package.json"),
    (["/x/a/package.json", "/x/b/package.json"], {"base_paths": ["/x/a", "/x/b"]}, "package.json"),
    ([r"C:\repo\package.json", "C:/repo/package.json"], {"base_path": r"C:\repo"}, "package.json"),
    (["./package.json", "package.json"], {}, "package.json"),
    (['/repo/a"b/package.json', "/repo/a%22b/package.json"], {"base_path": "/repo"}, "a%22b/package.json"),
    (["/repo/a\nb/package.json", "/repo/a%0Ab/package.json"], {"base_path": "/repo"}, "a%0Ab/package.json"),
    (["/repo/a\rb/package.json", "/repo/a%0Db/package.json"], {"base_path": "/repo"}, "a%0Db/package.json"),
    (["/repo/package.json", "/repo//package.json"], {"workspace": "/repo"}, "package.json"),
]


def assert_collision(error, key, paths):
    assert str(error.value) == (
        f"Duplicate upload key '{key}' from '{paths[0]}' and '{paths[1]}'"
    )


@pytest.mark.parametrize("paths,options,key", COLLISIONS)
def test_lazy_utility_rejects_collisions_before_creating_loaders(paths, options, key):
    with patch("socketdev.utils.LazyFileLoader") as loader:
        with pytest.raises(ValueError) as error:
            Utils.load_files_for_sending_lazy(paths, **options)
    assert_collision(error, key, paths)
    loader.assert_not_called()


@pytest.mark.parametrize("paths,options,key", COLLISIONS)
@pytest.mark.parametrize("lazy", [True, False])
def test_manifest_upload_rejects_collisions_before_reading_or_sending(paths, options, key, lazy):
    api = Mock()
    with patch("os.path.exists", return_value=True), patch("os.path.isfile", return_value=True):
        with patch("builtins.open") as opened:
            with pytest.raises(ValueError) as error:
                UploadManifests(api).upload_manifest_files("org", paths, use_lazy_loading=lazy, **options)
    assert_collision(error, key, paths)
    opened.assert_not_called()
    api.do_request.assert_not_called()


@pytest.mark.parametrize("paths,options,key", COLLISIONS)
def test_fullscan_rejects_collisions_before_sending(paths, options, key):
    api = Mock()
    with pytest.raises(ValueError) as error:
        FullScans(api).post(paths, FullScanParams(repo="repo", org_slug="org"), use_lazy_loading=True, **options)
    assert_collision(error, key, paths)
    api.do_request.assert_not_called()


@pytest.mark.parametrize("lazy", [True, False])
def test_clean_manifest_upload_preserves_keys_order_and_contents(tmp_path, lazy):
    paths = [tmp_path / "frontend" / "package.json", tmp_path / "backend" / "package.json"]
    for i, path in enumerate(paths):
        path.parent.mkdir()
        path.write_bytes(f"manifest {i}".encode())
    api = Mock()
    api.do_request.return_value.status_code = 200
    api.do_request.return_value.json.return_value = {"tarHash": "hash"}
    assert UploadManifests(api).upload_manifest_files(
        "org", [str(path) for path in paths], base_path=str(tmp_path), use_lazy_loading=lazy
    ) == "hash"
    files = api.do_request.call_args.kwargs["files"]
    assert [key for key, _ in files] == ["frontend/package.json", "backend/package.json"]
    for i, (key, (filename, content)) in enumerate(files):
        assert filename == key
        if lazy:
            try:
                assert content.read() == f"manifest {i}".encode()
            finally:
                content.close()
        else:
            assert content == f"manifest {i}".encode()


def test_clean_fullscan_preserves_lazy_multipart_keys(tmp_path):
    paths = [str(tmp_path / "a" / "package.json"), str(tmp_path / "b" / "package.json")]
    api = Mock()
    api.do_request.return_value.status_code = 201
    api.do_request.return_value.json.return_value = {"id": "scan"}
    assert FullScans(api).post(
        paths, FullScanParams(repo="repo", org_slug="org"), use_lazy_loading=True, base_path=str(tmp_path)
    ) == {"id": "scan"}
    files = api.do_request.call_args.kwargs["files"]
    assert [(key, value[0], value[1].file_path) for key, value in files] == [
        ("a/package.json", "a/package.json", paths[0]),
        ("b/package.json", "b/package.json", paths[1]),
    ]


def test_lazy_utility_skips_directories(tmp_path):
    directory = str(tmp_path)
    assert Utils.load_files_for_sending_lazy([directory, directory]) == []


def test_prepared_fullscan_rejects_duplicate_keys():
    api = Mock()
    files = [("package.json", (path, BytesIO(b"{}"))) for path in ("/a/package.json", "/b/package.json")]
    with pytest.raises(ValueError) as error:
        FullScans(api).post(files, FullScanParams(repo="repo", org_slug="org"))
    assert_collision(error, "package.json", ["/a/package.json", "/b/package.json"])
    assert all(value[1].tell() == 0 for _, value in files)
    api.do_request.assert_not_called()


@pytest.mark.parametrize("mapping", [True, False])
def test_prepared_fullscan_preserves_valid_files(mapping):
    api = Mock()
    api.do_request.return_value.status_code = 201
    files = [("a/package.json", ("a/package.json", b"{}")), ("b/package.json", BytesIO(b"{}"))]
    if mapping:
        files = dict(files)
    FullScans(api).post(files, FullScanParams(repo="repo", org_slug="org"))
    assert api.do_request.call_args.kwargs["files"] is files


@pytest.mark.parametrize("shape", ["iterator", "mapping", "none", "tuple-none", "metadata", "list-value"])
def test_prepared_fullscan_preserves_encoded_parts(shape):
    part = ("package.json", ("package.json", b"manifest content"))
    entries = [part]
    if shape == "none":
        entries.insert(0, ("package.json", None))
    elif shape == "tuple-none":
        entries.insert(0, ("package.json", ("missing.json", None)))
    elif shape == "metadata":
        entries = [("package.json", ("package.json", b"manifest content", "application/json", {"X-Manifest": "yes"}))]
    elif shape == "list-value":
        entries = [("package.json", ["package.json", b"manifest content"])]
    files = iter(entries) if shape == "iterator" else UserDict(entries) if shape == "mapping" else entries
    api = Mock()
    api.do_request.return_value.status_code = 201
    FullScans(api).post(files, FullScanParams(repo="repo", org_slug="org"))
    forwarded = api.do_request.call_args.kwargs["files"]
    # A fixed boundary makes the encoded body comparable byte for byte.
    with patch("urllib3.filepost.choose_boundary", return_value="test-boundary"):
        expected = Request("POST", "https://example.test", files=entries).prepare()
        actual = Request("POST", "https://example.test", files=forwarded).prepare()
    assert actual.body == expected.body
    assert actual.body.count(b'name="package.json";') == 1


def test_prepared_fullscan_rejects_equivalent_byte_and_string_keys():
    api = Mock()
    files = [("package.json", ("a.json", b"first")), (b"package.json", ("b.json", b"second"))]
    with pytest.raises(ValueError) as error:
        FullScans(api).post(files, FullScanParams(repo="repo", org_slug="org"))
    assert_collision(error, "package.json", ["a.json", "b.json"])
    api.do_request.assert_not_called()


@pytest.mark.parametrize("character,escape", [('"', "%22"), ("\n", "%0A"), ("\r", "%0D")])
def test_prepared_fullscan_rejects_keys_with_identical_encoded_names(character, escape):
    keys = [f"a{character}b/package.json", f"a{escape}b/package.json"]
    files = [(keys[0], ("a.json", b"first")), (keys[1], ("b.json", b"second"))]
    encoded = Request("POST", "https://example.test", files=files).prepare()
    assert encoded.body.count(f'name="{keys[1]}";'.encode()) == 2
    api = Mock()
    with pytest.raises(ValueError) as error:
        FullScans(api).post(files, FullScanParams(repo="repo", org_slug="org"))
    assert_collision(error, keys[1], ["a.json", "b.json"])
    api.do_request.assert_not_called()


@pytest.mark.parametrize("prepared", [True, False])
def test_collision_validation_uses_installed_encoder(prepared):
    def legacy_formatter(name, value):
        replacements = {code: f"%{code:02X}" for code in range(32) if code != 27}
        replacements.update({34: "%22", 92: "\\\\"})
        return f'{name}="{value.translate(replacements)}"'

    keys = ["a\tb/package.json", "a%09b/package.json"]
    files = [(keys[0], ("a.json", b"first")), (keys[1], ("b.json", b"second"))]
    api = Mock()
    original_init = RequestField.__init__

    def legacy_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.header_formatter = legacy_formatter

    with patch.object(RequestField, "__init__", legacy_init):
        encoded = Request("POST", "https://example.test", files=files).prepare()
        assert encoded.body.count(b'name="a%09b/package.json";') == 2
        with pytest.raises(ValueError) as error:
            if prepared:
                FullScans(api).post(files, FullScanParams(repo="repo", org_slug="org"))
            else:
                Utils.load_files_for_sending_lazy(keys)
    assert_collision(error, keys[1], ["a.json", "b.json"] if prepared else keys)
    api.do_request.assert_not_called()


def test_prepared_fullscan_preserves_unnamed_part():
    api = Mock()
    api.do_request.return_value.status_code = 201
    files = [(None, ("package.json", b"manifest content"))]
    FullScans(api).post(files, FullScanParams(repo="repo", org_slug="org"))
    forwarded = api.do_request.call_args.kwargs["files"]
    with patch("urllib3.filepost.choose_boundary", return_value="test-boundary"):
        assert Request("POST", "https://example.test", files=files).prepare().body == Request(
            "POST", "https://example.test", files=forwarded
        ).prepare().body
