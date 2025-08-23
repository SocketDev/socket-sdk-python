
socketdev
#########

Purpose
-------

The Socket.dev Python SDK provides a wrapper around the Socket.dev REST API to simplify making calls to the API from Python.

Socket API v0 - https://docs.socket.dev/reference/introduction-to-socket-api

Initializing the module
-----------------------

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME", timeout=30)

**PARAMETERS:**

- **token (str)** - The Socket API Key for your Organization
- **Timeout (int)** - The number of seconds to wait before failing the connection

Supported Functions
-------------------


purl.post(license, components)
""""""""""""""""""""""""""""""
Retrieve the package information for a purl post

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    license = "true"
    components = [
        {
        "purl": "pkg:pypi/pyonepassword@5.0.0"
        },
        {
        "purl": "pkg:pypi/socketsecurity"
        }
    ]
    print(socket.purl.post(license, components))

**PARAMETERS:**

- **license (str)** - The license parameter if enabled will show alerts and license information. If disabled will only show the basic package metadata and scores. Default is true
- **components (array{dict})** - The components list of packages urls

export.cdx_bom(org_slug, id, query_params)
""""""""""""""""""""""""""""""""""""""""""
Export a Socket SBOM as a CycloneDX SBOM

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    from socketdev.export import ExportQueryParams

    socket = socketdev(token="REPLACE_ME")
    query_params = ExportQueryParams(
        author="john_doe",
        project_name="my-project"
    )
    print(socket.export.cdx_bom("org_slug", "sbom_id", query_params))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **id (str)** - The ID of either a full scan or an SBOM report
- **query_params (ExportQueryParams)** - Optional query parameters for filtering:
    - **author (str)** - Filter by author
    - **project_group (str)** - Filter by project group
    - **project_name (str)** - Filter by project name
    - **project_version (str)** - Filter by project version
    - **project_id (str)** - Filter by project ID

export.spdx_bom(org_slug, id, query_params)
"""""""""""""""""""""""""""""""""""""""""""
Export a Socket SBOM as an SPDX SBOM

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    from socketdev.export import ExportQueryParams

    socket = socketdev(token="REPLACE_ME")
    query_params = ExportQueryParams(
        project_name="my-project",
        project_version="1.0.0"
    )
    print(socket.export.spdx_bom("org_slug", "sbom_id", query_params))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **id (str)** - The ID of either a full scan or an SBOM report
- **query_params (ExportQueryParams)** - Optional query parameters for filtering:
    - **author (str)** - Filter by author
    - **project_group (str)** - Filter by project group
    - **project_name (str)** - Filter by project name
    - **project_version (str)** - Filter by project version
    - **project_id (str)** - Filter by project ID

fullscans.get(org_slug)
"""""""""""""""""""""""
Retrieve the Fullscans information for around Organization

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.get("org_slug"))

**PARAMETERS:**

- **org_slug (str)** - The organization name

fullscans.post(files, params)
"""""""""""""""""""""""""""""
Create a full scan from a set of package manifest files. Returns a full scan including all SBOM artifacts.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    files = [
        "/path/to/manifest/package.json"
    ]
    params = {
    "org_slug": "org_name",
    "repo": "TestRepo",
    "branch": "main",
    "commit_message": "Test Commit Message",
    "commit_hash": "",
    "pull_request": "",
    "committers": "commiter",
    "make_default_branch": False,
    "set_as_pending_head": False,
    "tmp": ""
    }

    print(socket.fullscans.post(files, params))

**PARAMETERS:**

- **files (list)** - List of file paths of manifest files
- **params (dict)** - List of parameters to create a fullscan

+------------------------+------------+-------------------------------------------------------------------------------+
| Parameter              | Required   | Description                                                                   |
+========================+============+===============================================================================+
| org_slug               | True       | The string name in a git approved name for organization.                      |
+------------------------+------------+-------------------------------------------------------------------------------+
| repo                   | True       | The string name in a git approved name for repositories.                      |
+------------------------+------------+-------------------------------------------------------------------------------+
| branch                 | False      | The string name in a git approved name for branches.                          |
+------------------------+------------+-------------------------------------------------------------------------------+
| committers             | False      | The string name of the person doing the commit or running the CLI.            |
|                        |            | Can be specified multiple times to have more than one committer.              |
+------------------------+------------+-------------------------------------------------------------------------------+
| pull_request           | False      | The integer for the PR or MR number.                                          |
+------------------------+------------+-------------------------------------------------------------------------------+
| commit_message         | False      | The string for a commit message if there is one.                              |
+------------------------+------------+-------------------------------------------------------------------------------+
| make_default_branch    | False      | If the flag is specified this will signal that this is the default branch.    |
+------------------------+------------+-------------------------------------------------------------------------------+
| commit_hash            | False      | Optional git commit hash                                                      |
+------------------------+------------+-------------------------------------------------------------------------------+
| set_as_pending_head    | False      |                                                                               |
+------------------------+------------+-------------------------------------------------------------------------------+
| tmp                    | False      |                                                                               |
+------------------------+------------+-------------------------------------------------------------------------------+

fullscans.delete(org_slug, full_scan_id)
""""""""""""""""""""""""""""""""""""""""
Delete an existing full scan.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.delete(org_slug, full_scan_id))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **full_scan_id (str)** - The ID of the full scan

fullscans.stream_diff(org_slug, before, after, preview, include_license_details)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Stream a diff between two full scans. Returns a scan diff.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.stream_diff("org_slug", "before_scan_id", "after_scan_id"))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **before (str)** - The base full scan ID
- **after (str)** - The comparison full scan ID
- **include_license_details (bool)** - Include license details. Can greatly increase response size. Defaults to False.

fullscans.stream(org_slug, full_scan_id)
""""""""""""""""""""""""""""""""""""""""
Stream all SBOM artifacts for a full scan.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.stream(org_slug, full_scan_id))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **full_scan_id (str)** - The ID of the full scan

fullscans.metadata(org_slug, full_scan_id)
""""""""""""""""""""""""""""""""""""""""""
Get metadata for a single full scan

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.metadata(org_slug, full_scan_id))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **full_scan_id (str)** - The ID of the full scan

dependencies.get(limit, offset)
"""""""""""""""""""""""""""""""
Retrieve the dependencies for the organization associated with the API Key

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.dependencies.get(10, 0))

**PARAMETERS:**

- **limit (int)** - The maximum number of dependencies to return
- **offset (int)** - The index to start from for pulling the dependencies

dependencies.post(files, params)
""""""""""""""""""""""""""""""""
Retrieve the dependencies for the organization associated with the API Key

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    file_names = [
        "path/to/package.json"
    ]
    params = {
        "repository": "username/repo-name",
        "branch": "dependency-branch
    }
    print(socket.dependencies.post(file_names, params))

**PARAMETERS:**

- **files (list)** - The file paths of the manifest files to import into the Dependency API.
- **params (dict)** - A dictionary of the `repository` and `branch` options for the API

repos.get()
"""""""""""
Get a list of information about the tracked repositores

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.repos.get(sort="name", direction="asc", per_page=100, page=1))

**PARAMETERS:**

- **sort** - The key to sort on froom the repo properties. Defaults to `created_at`
- **direction** - Can be `desc` or `asc`. Defaults to `desc`
- **per_page** - Integer between 1 to 100. Defaults to `10`
- **page** - Integer page number defaults to `1`. If there are no more results it will be `0`

repos.post()
""""""""""""
Create a new Socket Repository

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(
        socket.repos.post(
            name="example",
            description="Info about Repo",
            homepage="http://homepage",
            visibility='public',
            archived=False,
            default_branch='not-main'
        )
    )

**PARAMETERS:**

- **name(required)** - The name of the Socket Repository
- **description(optional)** - String description of the repository
- **homepage(optional)** - URL of the homepage of the
- **visibility(optional)** - Can be `public` or `private` and defaults to `private`
- **archived(optional)** - Boolean on if the repository is archived. Defaults to `False`
- **default_branch(optional)** - String name of the default branch for the repository. Defaults to `main`

repos.repo()
""""""""""""
Get a list of information about the tracked repositores

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.repos.repo(org_slug="example", repo_name="example-repo")

repos.update()
""""""""""""""
Update an existing Socket Repository

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(
        socket.repos.update(
            org_slug="example-org",
            repo_name="example",
            name="new-name-example",
            description="Info about Repo",
            homepage="http://homepage",
            visibility='public',
            archived=False,
            default_branch='not-main'
        )
    )

- **name(optional)** - The name of the Socket Repository
- **description(optional)** - String description of the repository
- **homepage(optional)** - URL of the homepage of the
- **visibility(optional)** - Can be `public` or `private` and defaults to `private`
- **archived(optional)** - Boolean on if the repository is archived. Defaults to `False`
- **default_branch(optional)** - String name of the default branch for the repository. Defaults to `main`

repos.delete()
""""""""""""""
Delete a Socket Repository

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.repos.delete(org_slug="example", repo_name="example-repo")

**PARAMETERS:**

- **org_slug** - Name of the Socket Org
- **repo_name** - The name of the Socket Repository to delete

org.get()
"""""""""
Retrieve the Socket.dev org information

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.org.get())

quota.get()
"""""""""""
Retrieve the the current quota available for your API Key

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.quota.get())

settings.get()
""""""""""""""
Retrieve the Socket Organization Settings

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.settings.get())

report.supported()
""""""""""""""""""
Retrieve the supported types of manifest files for creating a report

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.report.supported())

Deprecated: report.list()
"""""""""""""""""""""""""
Retrieve the list of all reports for the organization

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.report.list(from_time=1726183485))

**PARAMETERS:**

- **from_time (int)** - The Unix Timestamp in Seconds to limit the reports pulled

Deprecated: report.delete(report_id)
""""""""""""""""""""""""""""""""""""
Delete the specified report

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.report.delete("report-id"))

**PARAMETERS:**

- **report_id (str)** - The report ID of the report to delete

Deprecated: report.view(report_id)
""""""""""""""""""""""""""""""""""
Retrieve the information for a Project Health Report

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.report.view("report_id"))

**PARAMETERS:**

- **report_id (str)** - The report ID of the report to view

Deprecated: report.create(files)
""""""""""""""""""""""""""""""""
Create a new project health report with the provided files

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    files = [
        "/path/to/manifest/package.json"
    ]
    print(socket.report.create(files))

**PARAMETERS:**

- **files (list)** - List of file paths of manifest files

Deprecated: repositories.get()
""""""""""""""""""""""""""""""
Get a list of information about the tracked repositores

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.repositories.get())

Deprecated: sbom.view(report_id)
""""""""""""""""""""""""""""""""
Retrieve the information for a SBOM Report

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.sbom.view("report_id"))

Deprecated: npm.issues(package, version)
""""""""""""""""""""""""""""""""""""""""
Retrieve the Issues associated with a package and version.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.npm.issues("hardhat-gas-report", "1.1.25"))

**PARAMETERS:**

- **package (str)** - The name of the NPM package.
- **version (str)** - The version of the NPM Package.

Deprecated: npm.score(package, version)
"""""""""""""""""""""""""""""""""""""""
Retrieve the Issues associated with a package and version.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.npm.score("hardhat-gas-report", "1.1.25"))

**PARAMETERS:**

- **package (str)** - The name of the NPM package.
- **version (str)** - The version of the NPM Package.

labels.list(org_slug)
"""""""""""""""""""""""
List all repository labels for the given organization.

**Usage:**

.. code-block:: python

    from socketdev import socketdev

    socket = socketdev(token="REPLACE_ME")
    print(socket.labels.list("org_slug"))

**PARAMETERS:**

- **org_slug (str)** – The organization name

labels.post(org_slug, label_name)
"""""""""""""""""""""""""""""""""""
Create a new label in the organization.

**Usage:**

.. code-block:: python

    print(socket.labels.post("org_slug", "my-label"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **label_name (str)** – Name of the label to create

labels.get(org_slug, label_id)
"""""""""""""""""""""""""""""""""
Retrieve a single label by its ID.

**Usage:**

.. code-block:: python

    print(socket.labels.get("org_slug", "label_id"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **label_id (str)** – The label ID

labels.delete(org_slug, label_id)
"""""""""""""""""""""""""""""""""""
Delete a label by ID.

**Usage:**

.. code-block:: python

    print(socket.labels.delete("org_slug", "label_id"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **label_id (str)** – The label ID

labels.associate(org_slug, label_id, repo_id)
"""""""""""""""""""""""""""""""""""""""""""""""
Associate a label with a repository.

**Usage:**

.. code-block:: python

    print(socket.labels.associate("org_slug", 1234, "repo_id"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **label_id (int)** – The label ID
- **repo_id (str)** – The repository ID

labels.disassociate(org_slug, label_id, repo_id)
"""""""""""""""""""""""""""""""""""""""""""""""""
Disassociate a label from a repository.

**Usage:**

.. code-block:: python

    print(socket.labels.disassociate("org_slug", 1234, "repo_id"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **label_id (int)** – The label ID
- **repo_id (str)** – The repository ID

labels.setting.get(org_slug, label_id, setting_key)
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Get a setting for a specific label.

**Usage:**

.. code-block:: python

    print(socket.labels.setting.get("org_slug", 1234, "severity"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **label_id (int)** – The label ID
- **setting_key (str)** – The key of the setting

labels.setting.put(org_slug, label_id, settings)
"""""""""""""""""""""""""""""""""""""""""""""""""""
Update settings for a specific label.

**Usage:**

.. code-block:: python

    settings = {"severity": {"value": {"level": "high"}}}
    print(socket.labels.setting.put("org_slug", 1234, settings))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **label_id (int)** – The label ID
- **settings (dict)** – A dictionary of label settings

labels.setting.delete(org_slug, label_id, setting_key)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
Delete a setting from a label.

**Usage:**

.. code-block:: python

    print(socket.labels.setting.delete("org_slug", 1234, "severity"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **label_id (int)** – The label ID
- **setting_key (str)** – The setting key to delete

historical.list(org_slug, query_params=None)
"""""""""""""""""""""""""""""""""""""""""""""""
List historical alerts for an organization.

**Usage:**

.. code-block:: python

    print(socket.historical.list("org_slug", {"repo": "example-repo"}))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **query_params (dict, optional)** – Optional query parameters

historical.trend(org_slug, query_params=None)
"""""""""""""""""""""""""""""""""""""""""""""""
Retrieve alert trend data across time.

**Usage:**

.. code-block:: python

    print(socket.historical.trend("org_slug", {"range": "30d"}))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **query_params (dict, optional)** – Optional query parameters

historical.snapshots.create(org_slug)
""""""""""""""""""""""""""""""""""""""""
Create a new snapshot of historical data.

**Usage:**

.. code-block:: python

    print(socket.historical.snapshots.create("org_slug"))

**PARAMETERS:**

- **org_slug (str)** – The organization name

historical.snapshots.list(org_slug, query_params=None)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
List all historical snapshots for an organization.

**Usage:**

.. code-block:: python

    print(socket.historical.snapshots.list("org_slug", {"repo": "example-repo"}))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **query_params (dict, optional)** – Optional query parameters
