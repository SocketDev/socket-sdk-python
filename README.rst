
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

fullscans.get(org_slug, params)
"""""""""""""""""""""""""""""""
Retrieve the Fullscans information for an Organization with query parameters

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    
    # Query parameters for filtering full scans
    params = {
        "repo": "my-repo",
        "branch": "main",
        "limit": 10,
        "offset": 0
    }
    print(socket.fullscans.get("org_slug", params))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **params (dict)** - Query parameters for filtering results (required)

fullscans.post(files, params)
"""""""""""""""""""""""""""""
Create a full scan from a set of package manifest files. Returns a full scan including all SBOM artifacts.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    from socketdev.fullscans import FullScanParams
    
    socket = socketdev(token="REPLACE_ME")
    files = [
        "/path/to/manifest/package.json"
    ]
    params = FullScanParams(
        org_slug="org_name",
        repo="TestRepo",
        branch="main",
        commit_message="Test Commit Message",
        commit_hash="abc123def456",
        pull_request=123,
        committers=["committer1", "committer2"],
        make_default_branch=False,
        set_as_pending_head=False
    )

    print(socket.fullscans.post(files, params))

**PARAMETERS:**

- **files (list)** - List of file paths of manifest files
- **params (FullScanParams)** - FullScanParams object containing scan configuration

+------------------------+------------+-------------------------------------------------------------------------------+
| Parameter              | Required   | Description                                                                   |
+========================+============+===============================================================================+
| org_slug               | True       | The string name in a git approved name for organization.                      |
+------------------------+------------+-------------------------------------------------------------------------------+
| repo                   | True       | The string name in a git approved name for repositories.                      |
+------------------------+------------+-------------------------------------------------------------------------------+
| branch                 | False      | The string name in a git approved name for branches.                          |
+------------------------+------------+-------------------------------------------------------------------------------+
| committers             | False      | List of committer names (List[str]).                                          |
+------------------------+------------+-------------------------------------------------------------------------------+
| pull_request           | False      | The integer for the PR or MR number.                                          |
+------------------------+------------+-------------------------------------------------------------------------------+
| commit_message         | False      | The string for a commit message if there is one.                              |
+------------------------+------------+-------------------------------------------------------------------------------+
| make_default_branch    | False      | Boolean to signal that this is the default branch.                            |
+------------------------+------------+-------------------------------------------------------------------------------+
| commit_hash            | False      | Optional git commit hash                                                      |
+------------------------+------------+-------------------------------------------------------------------------------+
| set_as_pending_head    | False      | Boolean to set as pending head                                                |
+------------------------+------------+-------------------------------------------------------------------------------+
| tmp                    | False      | Boolean temporary flag                                                        |
+------------------------+------------+-------------------------------------------------------------------------------+
| integration_type       | False      | IntegrationType enum value (e.g., "api", "github")                            |
+------------------------+------------+-------------------------------------------------------------------------------+
| integration_org_slug   | False      | Organization slug for integration                                             |
+------------------------+------------+-------------------------------------------------------------------------------+

fullscans.delete(org_slug, full_scan_id)
""""""""""""""""""""""""""""""""""""""""
Delete an existing full scan.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.delete("org_slug", "full_scan_id"))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **full_scan_id (str)** - The ID of the full scan

fullscans.stream_diff(org_slug, before, after, use_types=True, include_license_details="true", \*\*kwargs)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Stream a diff between two full scans. Returns a scan diff.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.stream_diff("org_slug", "before_scan_id", "after_scan_id"))
    
    # With additional parameters
    print(socket.fullscans.stream_diff(
        "org_slug", 
        "before_scan_id", 
        "after_scan_id",
        use_types=False,
        include_license_details="false"
    ))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **before (str)** - The base full scan ID
- **after (str)** - The comparison full scan ID
- **use_types (bool)** - Whether to return typed response objects (default: True)
- **include_license_details (str)** - Include license details ("true"/"false"). Can greatly increase response size. Defaults to "true".
- **kwargs** - Additional query parameters

fullscans.stream(org_slug, full_scan_id, use_types=False)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Stream all SBOM artifacts for a full scan.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.stream("org_slug", "full_scan_id"))
    
    # With typed response
    print(socket.fullscans.stream("org_slug", "full_scan_id", use_types=True))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **full_scan_id (str)** - The ID of the full scan
- **use_types (bool)** - Whether to return typed response objects (default: False)

fullscans.metadata(org_slug, full_scan_id, use_types=False)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Get metadata for a single full scan

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.metadata("org_slug", "full_scan_id"))
    
    # With typed response
    print(socket.fullscans.metadata("org_slug", "full_scan_id", use_types=True))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **full_scan_id (str)** - The ID of the full scan
- **use_types (bool)** - Whether to return typed response objects (default: False)

fullscans.gfm(org_slug, before, after)
""""""""""""""""""""""""""""""""""""""
Get GitHub Flavored Markdown diff between two full scans.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.fullscans.gfm("org_slug", "before_scan_id", "after_scan_id"))

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **before (str)** - The base full scan ID
- **after (str)** - The comparison full scan ID

basics.get_config(org_slug, use_types)
""""""""""""""""""""""""""""""""""""""
Get Socket Basics configuration for an organization. Socket Basics is a CI/CD security scanning suite that includes SAST scanning, secret detection, container security, and dependency analysis.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    
    # Basic usage - returns dictionary
    config = socket.basics.get_config("org_slug")
    print(f"Python SAST enabled: {config['pythonSastEnabled']}")
    print(f"Secret scanning enabled: {config['secretScanningEnabled']}")
    
    # Using typed response objects
    from socketdev.basics import SocketBasicsConfig, SocketBasicsResponse
    response = socket.basics.get_config("org_slug", use_types=True)
    if response.success and response.config:
        print(f"JavaScript SAST: {response.config.javascriptSastEnabled}")
        print(f"Trivy scanning: {response.config.trivyImageEnabled}")

**PARAMETERS:**

- **org_slug (str)** - The organization name
- **use_types (bool)** - Whether to return typed response objects (default: False)

**Socket Basics Features:**

- **Python SAST** - Static analysis for Python code
- **Go SAST** - Static analysis for Go code  
- **JavaScript SAST** - Static analysis for JavaScript/TypeScript code
- **Secret Scanning** - Detection of hardcoded secrets and credentials
- **Trivy Image Scanning** - Vulnerability scanning for Docker images
- **Trivy Dockerfile Scanning** - Vulnerability scanning for Dockerfiles
- **Socket SCA** - Supply chain analysis for dependencies
- **Socket Scanning** - General dependency security scanning
- **Additional Parameters** - Custom configuration options

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
        "branch": "dependency-branch"
    }
    print(socket.dependencies.post(file_names, params))

**PARAMETERS:**

- **files (list)** - The file paths of the manifest files to import into the Dependency API.
- **params (dict)** - A dictionary of the `repository` and `branch` options for the API

repos.get()
"""""""""""
Get a list of information about the tracked repositories

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.repos.get(sort="name", direction="asc", per_page=100, page=1))

**PARAMETERS:**

- **sort** - The key to sort on from the repo properties. Defaults to `created_at`
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
Get a list of information about the tracked repositories

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.repos.repo(org_slug="example", repo_name="example-repo"))

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
    print(socket.repos.delete(org_slug="example", repo_name="example-repo"))

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
Get a list of information about the tracked repositories

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

diffscans.list(org_slug, params=None)
"""""""""""""""""""""""""""""""""""""
List all diff scans for an organization.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.diffscans.list("org_slug", {"limit": 10, "offset": 0}))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **params (dict, optional)** – Optional query parameters for filtering

diffscans.get(org_slug, diff_scan_id)
"""""""""""""""""""""""""""""""""""""
Fetch a specific diff scan by ID.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.diffscans.get("org_slug", "diff_scan_id"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **diff_scan_id (str)** – The ID of the diff scan to retrieve

diffscans.create_from_ids(org_slug, params)
"""""""""""""""""""""""""""""""""""""""""""
Create a diff scan from two full scan IDs.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    params = {
        "before": "full_scan_id_1",
        "after": "full_scan_id_2",
        "description": "Compare two scans"
    }
    print(socket.diffscans.create_from_ids("org_slug", params))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **params (dict)** – Parameters including before and after scan IDs

diffscans.create_from_repo(org_slug, repo_slug, files, params=None)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Create a diff scan from repository files.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    files = ["/path/to/package.json"]
    params = {"branch": "main", "commit": "abc123"}
    print(socket.diffscans.create_from_repo("org_slug", "repo_slug", files, params))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **repo_slug (str)** – The repository name
- **files (list)** – List of file paths to scan
- **params (dict, optional)** – Optional parameters for the scan

diffscans.gfm(org_slug, diff_scan_id)
"""""""""""""""""""""""""""""""""""""
Get GitHub Flavored Markdown comments for a diff scan.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.diffscans.gfm("org_slug", "diff_scan_id"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **diff_scan_id (str)** – The ID of the diff scan

diffscans.delete(org_slug, diff_scan_id)
""""""""""""""""""""""""""""""""""""""""
Delete a specific diff scan.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.diffscans.delete("org_slug", "diff_scan_id"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **diff_scan_id (str)** – The ID of the diff scan to delete

threatfeed.get(org_slug=None, \*\*kwargs)
"""""""""""""""""""""""""""""""""""""""""""
Get threat feed items for an organization or globally.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    
    # Get org-specific threat feed
    print(socket.threatfeed.get("org_slug", per_page=50, sort="created_at"))
    
    # Get global threat feed (deprecated)
    print(socket.threatfeed.get())

**PARAMETERS:**

- **org_slug (str, optional)** – The organization name (recommended for new implementations)
- **kwargs** – Query parameters like per_page, page_cursor, sort, etc.

apitokens.create(org_slug, \*\*kwargs)
""""""""""""""""""""""""""""""""""""""
Create a new API token for an organization.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    token_config = {
        "name": "My API Token",
        "permissions": ["read", "write"],
        "expires_at": "2024-12-31T23:59:59Z"
    }
    print(socket.apitokens.create("org_slug", **token_config))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **kwargs** – Token configuration parameters

apitokens.update(org_slug, \*\*kwargs)
""""""""""""""""""""""""""""""""""""""
Update an existing API token.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    update_params = {
        "token_id": "token_123",
        "name": "Updated Token Name",
        "permissions": ["read"]
    }
    print(socket.apitokens.update("org_slug", **update_params))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **kwargs** – Token update parameters

auditlog.get(org_slug, \*\*kwargs)
""""""""""""""""""""""""""""""""""""
Get audit log entries for an organization.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.auditlog.get("org_slug", limit=100, cursor="abc123"))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **kwargs** – Query parameters like limit, cursor, etc.

analytics.get_org(filter, \*\*kwargs)
"""""""""""""""""""""""""""""""""""""""
Get organization analytics (deprecated - use Historical module instead).

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    # DEPRECATED: Use socket.historical.list() or socket.historical.trend() instead
    print(socket.analytics.get_org("alerts", start_date="2024-01-01"))

**PARAMETERS:**

- **filter (str)** – Analytics filter type
- **kwargs** – Additional query parameters

analytics.get_repo(name, filter, \*\*kwargs)
""""""""""""""""""""""""""""""""""""""""""""""
Get repository analytics (deprecated - use Historical module instead).

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    # DEPRECATED: Use socket.historical.list() or socket.historical.trend() instead
    print(socket.analytics.get_repo("repo_name", "alerts", start_date="2024-01-01"))

**PARAMETERS:**

- **name (str)** – Repository name
- **filter (str)** – Analytics filter type
- **kwargs** – Additional query parameters

alerttypes.get(alert_types=None, language="en-US", \*\*kwargs)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Get alert types metadata.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    
    # Get metadata for specific alert types
    alert_list = ["supply_chain_risk", "license_risk"]
    print(socket.alerttypes.get(alert_list, language="en-US"))
    
    # Get all alert types metadata
    print(socket.alerttypes.get())

**PARAMETERS:**

- **alert_types (list, optional)** – List of alert type strings to get metadata for
- **language (str)** – Language for alert metadata (default: en-US)
- **kwargs** – Additional query parameters

triage.list_alert_triage(org_slug, query_params=None)
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Get list of triaged alerts for an organization.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    query_params = {"status": "triaged", "limit": 50}
    print(socket.triage.list_alert_triage("org_slug", query_params))

**PARAMETERS:**

- **org_slug (str)** – The organization name
- **query_params (dict, optional)** – Optional query parameters for filtering

openapi.get()
"""""""""""""
Retrieve the OpenAPI specification for the Socket API.

**Usage:**

.. code-block:: python

    from socketdev import socketdev
    socket = socketdev(token="REPLACE_ME")
    print(socket.openapi.get())

**PARAMETERS:**

None required.
