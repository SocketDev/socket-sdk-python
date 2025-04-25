import json
import os
import logging
from socketdev import socketdev
logging.basicConfig(level=logging.INFO)


sdk = socketdev(token=os.getenv("SOCKET_SECURITY_API_KEY"))

orgs = sdk.org.get()
if len(orgs) > 0:
    org_id = None
    org_slug = None
    for org_key in orgs['organizations']:
        org = orgs['organizations'][org_key]
        org_id = org_key
        org_slug = org['slug']
else:
    print("Something went wrong with getting org info")
    exit(1)
per_page = 100
response = sdk.repos.get(org_slug, per_page=per_page)
next_page = response.get("nextPage")
repos = response.get("results")
while next_page is not None and next_page != 0:
    response = sdk.repos.get(org_slug, per_page=per_page, page=next_page)
    next_page = response.get("nextPage")
    repos.extend(response.get("results"))
    if len(response.get("results", [])) == 0:
        break

# repos = repos[:20]
head_full_scans_ids = []
for repo in repos:
    head_full_scans_id = repo.get("head_full_scan_id")
    if head_full_scans_id:
        head_full_scans_ids.append(head_full_scans_id)

socket_results = {}
for head_full_scan_id in head_full_scans_ids:
    full_scan_metadata = sdk.fullscans.metadata(org_slug=org_slug, full_scan_id=head_full_scan_id)
    full_scan_result = {
        "repo": full_scan_metadata.get("repo"),
        "branch": full_scan_metadata.get("branch"),
        "commit_hash": full_scan_metadata.get("commit_hash"),
        "commit_message": full_scan_metadata.get("commit_message"),
        "pull_request_url": full_scan_metadata.get("pull_request_url"),
        "committers": full_scan_metadata.get("committers"),
        "created_at": full_scan_metadata.get("created_at"),
        "results": sdk.fullscans.stream(org_slug=org_slug, full_scan_id=head_full_scan_id) or None
    }
    socket_results[head_full_scan_id] = full_scan_result

print(json.dumps(socket_results, indent=4))
