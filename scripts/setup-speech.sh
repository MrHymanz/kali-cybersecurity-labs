#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd -- "${script_dir}/.." && pwd)"
venv_dir="${project_dir}/.venv"
voice_dir="${project_dir}/voices"
config_file="${project_dir}/.tts.conf"
language="${1-}"

case "${language}" in
    en) voice_name="en_US-lessac-medium" ;;
    nl) voice_name="nl_NL-alex-medium" ;;
    *)
        printf '%s\n' 'Usage: setup-speech.sh en|nl' >&2
        exit 2
        ;;
esac

if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' 'Python 3 is required for speech support.' >&2
    exit 1
fi

if ! command -v pw-play >/dev/null 2>&1; then
    printf '%s\n' 'PipeWire (pw-play) is required for speech playback.' >&2
    exit 1
fi

if [[ ! -x "${venv_dir}/bin/python" ]]; then
    python3 -m venv "${venv_dir}"
fi

"${venv_dir}/bin/python" -m pip install --disable-pip-version-check --upgrade piper-tts
mkdir -p -- "${voice_dir}"
"${venv_dir}/bin/python" -m piper.download_voices --data-dir "${voice_dir}" "${voice_name}"
printf 'VOICE_NAME=%s\n' "${voice_name}" > "${config_file}"
printf 'Speech configured with %s.\n' "${voice_name}"
