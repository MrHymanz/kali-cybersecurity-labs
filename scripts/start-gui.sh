#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd -- "${script_dir}/.." && pwd)"
container_name="juice-shop"
target_url="http://127.0.0.1:3000/"

if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' 'Python 3 is required to start the graphical interface.' >&2
    exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
    printf '%s\n' 'Docker is required to run the Juice Shop lab target.' >&2
    exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
    printf '%s\n' 'curl is required to check whether the Juice Shop lab target is ready.' >&2
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    printf '%s\n' 'Docker is not running or your user cannot access the Docker daemon.' >&2
    printf '%s\n' 'Start Docker or correct your Docker permissions, then try again.' >&2
    exit 1
fi

if ! docker container inspect "${container_name}" >/dev/null 2>&1; then
    printf 'The Docker container %s does not exist.\n' "${container_name}" >&2
    printf '%s\n' 'Create the explicitly permitted Juice Shop lab target first, then try again.' >&2
    exit 1
fi

if [[ "$(docker inspect --format '{{.State.Running}}' "${container_name}")" != "true" ]]; then
    printf 'Starting the %s lab target...\n' "${container_name}"
    docker start "${container_name}" >/dev/null
fi

printf 'Waiting for the lab target at %s...\n' "${target_url}"
target_ready=false
for _ in {1..30}; do
    if curl --silent --show-error --fail --output /dev/null --max-time 2 "${target_url}" 2>/dev/null; then
        target_ready=true
        break
    fi
    sleep 1
done

if [[ "${target_ready}" != "true" ]]; then
    printf 'The %s container is running, but %s did not become reachable within 30 seconds.\n' \
        "${container_name}" "${target_url}" >&2
    printf 'Inspect it with: docker logs %s\n' "${container_name}" >&2
    exit 1
fi

printf '%s\n' 'The Juice Shop lab target is ready. Starting the graphical interface...'

exec python3 "${project_dir}/app/server.py"
