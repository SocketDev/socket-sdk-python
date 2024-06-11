
socketdev-python-sdk
###############

Purpose
-------

The Socket.dev Python SDK provides a wrapper around the Socket.dev REST API to simplify making calls to the API from Python.

Initializing the module
-----------------------

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")

Supported Functions
-------------------

npm.issues(package, version)
""""""""""""""""""""""""""""
Retrieve the Issues associated with a package and version.

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.npm.issues("hardhat-gas-report", "1.1.25"))

**PARAMETERS:**

- **package (str)** - The name of the NPM package.
- **version (str)** - The version of the NPM Package.

npm.score(package, version)
"""""""""""""""""""""""""""
Retrieve the Issues associated with a package and version.

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.npm.score("hardhat-gas-report", "1.1.25"))

**PARAMETERS:**

- **package (str)** - The name of the NPM package.
- **version (str)** - The version of the NPM Package.

dependencies.get(limit, offset)
""""""""""""""""""
Retrieve the dependencies for the organization associated with the API Key

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.dependencies.get(10, 0))

**PARAMETERS:**

- **limit (int)** - The maximum number of dependencies to return
- **offset (int)** - The index to start from for pulling the dependencies

dependencies.post(files, params)
""""""""""""""""""""""""""""""""
Retrieve the dependencies for the organization associated with the API Key

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
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

org.get()
"""""""""
Retrieve the Socket.dev org information

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.org.get())

quota.get()
"""""""""""
Retrieve the the current quota available for your API Key

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.quota.get())

report.list()
"""""""""""""
Retrieve the list of all reports for the organization

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.report.list())

report.delete(report_id)
""""""""""""""""""""""""
Delete the specified report

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.report.delete("report-id"))

**PARAMETERS:**

- **report_id (str)** - The report ID of the report to delete

report.view(report_id)
""""""""""""""""""""""
Retrieve the information for a Project Health Report

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.report.view("report_id"))

**PARAMETERS:**

- **report_id (str)** - The report ID of the report to view

report.supported()
""""""""""""""""""
Retrieve the supported types of manifest files for creating a report

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.report.supported())

report.create(files)
""""""""""""""""""""
Create a new project health report with the provided files

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    files = [
        "/path/to/manifest/package.json"
    ]
    print(socket.report.create(files))

**PARAMETERS:**

- **files (list)** - List of file paths of manifest files

repositories.get()
""""""""""""""""""
Get a list of information about the tracked repositores

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.repositories.get())

settings.get()
""""""""""""""
Retrieve the Socket Organization Settings

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.settings.get())

sbom.view(report_id)
""""""""""""""""""""""
Retrieve the information for a SBOM Report

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
    print(socket.sbom.view("report_id"))

**PARAMETERS:**

- **report_id (str)** - The report ID of the report to view

purl.post(license, components)
""""""""""""""""""""""
Retrieve the package information for a purl post

**Usage:**

.. code-block::

    from socketdev import SocketDev
    socket = SocketDev("REPLACE_ME")
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