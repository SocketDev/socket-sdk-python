#!/bin/sh

# Get version from version.py
VERSION_FILE="socketdev/version.py"
ORIGINAL_VERSION=$(grep -o "__version__.*" $VERSION_FILE | awk '{print $3}' | sed 's/"//g' | sed "s/'//g" | tr -d '\r')
BACKUP_FILE="${VERSION_FILE}.bak"

# Get existing versions from TestPyPI
echo "Checking existing versions on TestPyPI..."
EXISTING_VERSIONS=$(curl -s https://test.pypi.org/pypi/socket-sdk-python/json | python -c "
import sys, json
data = json.load(sys.stdin)
versions = [v for v in data.get('releases', {}).keys() if v.startswith('$ORIGINAL_VERSION.dev')]
if versions:
    versions.sort(key=lambda x: int(x.split('dev')[1]))
    print(versions[-1])
")

# Determine new version
if [ -z "$EXISTING_VERSIONS" ]; then
    VERSION="${ORIGINAL_VERSION}.dev1"
    echo "No existing dev versions found. Using ${VERSION}"
else
    LAST_DEV_NUM=$(echo $EXISTING_VERSIONS | grep -o 'dev[0-9]*' | grep -o '[0-9]*')
    NEXT_DEV_NUM=$((LAST_DEV_NUM + 1))
    VERSION="${ORIGINAL_VERSION}.dev${NEXT_DEV_NUM}"
    echo "Found existing version ${EXISTING_VERSIONS}. Using ${VERSION}"
fi

echo "Deploying version ${VERSION} to Test PyPI"

# Backup original version.py
cp $VERSION_FILE $BACKUP_FILE

# Update version in version.py
sed -i.tmp "s/__version__ = [\"']${ORIGINAL_VERSION}[\"']/__version__ = '${VERSION}'/" $VERSION_FILE
rm "${VERSION_FILE}.tmp"

# Build and upload to test PyPI (with suppressed output)
python -m build --wheel --sdist > /dev/null 2>&1

# Restore original version.py
mv $BACKUP_FILE $VERSION_FILE

# Upload to TestPyPI
python -m twine upload --verbose --repository testpypi dist/*${VERSION}*

echo "Deployed to Test PyPI. Wait a few minutes before installing the new version."
echo -e "\nNew version deployed:"
echo "${VERSION}" 