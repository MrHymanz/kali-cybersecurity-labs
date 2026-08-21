#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd -- "${script_dir}/.." && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' 'Python 3 is required to start the graphical interface.' >&2
    exit 1
fi

exec python3 "${project_dir}/app/server.py"
