#!/bin/bash
set -euxo pipefail
# Used by Zuul CI to perform extra bootstrapping

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Bumping system tox because version from CentOS 7 is too old
# We are not using pip --user due to few bugs in tox role which does not allow
# us to override how is called. Once these are addressed we will switch back
# non-sudo
command -v python3 python

PYTHON=$(command -v python3 python|head -n1)
PKG_CMD=$(command -v dnf yum|head -n1)

sudo $PYTHON -m pip install -U tox "zipp<0.6.0;python_version=='2.7'"

# Install latest goss version to /usr/local/bin
curl -fsSL https://goss.rocks/install | sudo sh
