#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd -- "${script_dir}/.." && pwd)"
venv_dir="${project_dir}/.venv"
voice_dir="${project_dir}/voices"
config_file="${project_dir}/.tts.conf"

lab_config_file="${project_dir}/.lab.conf"

printf '%s\n' 'Lesson language:'
printf '%s\n' '  1) English'
printf '%s\n' '  2) Nederlands (Dutch)'
printf 'Choose 1 or 2: '
read -r lesson_choice

case "${lesson_choice}" in
    1) lesson_language="en" ;;
    2) lesson_language="nl" ;;
    *)
        printf '%s\n' 'Invalid lesson-language choice; nothing was changed.' >&2
        exit 2
        ;;
esac

printf 'LESSON_LANGUAGE=%s\n' "${lesson_language}" > "${lab_config_file}"

printf '%s\n' 'Optional speech support:'
printf '%s\n' '  1) English (en_US-lessac-medium)'
printf '%s\n' '  2) Nederlands / Dutch (nl_NL-alex-medium)'
printf '%s\n' '  3) Disable speech'
printf 'Choose 1, 2 or 3: '
read -r choice

case "${choice}" in
    1) voice_name="en_US-lessac-medium" ;;
    2) voice_name="nl_NL-alex-medium" ;;
    3)
        rm -f -- "${config_file}"
        printf 'Setup complete. Lesson language: %s. Speech is disabled.\n' "${lesson_language}"
        printf '%s\n' 'Start the graphical interface with: ./scripts/start-gui.sh'
        exit 0
        ;;
    *)
        printf '%s\n' 'Invalid speech choice. The lesson-language preference was saved, but speech was not changed.' >&2
        exit 2
        ;;
esac

if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\n' 'Python 3 is missing. Install python3 and python3-venv first.' >&2
    exit 1
fi

if ! command -v pw-play >/dev/null 2>&1; then
    printf '%s\n' 'Warning: pw-play is missing; install PipeWire for audio output.' >&2
fi

if [[ ! -x "${venv_dir}/bin/python" ]]; then
    if ! python3 -m venv "${venv_dir}"; then
        printf '%s\n' 'Could not create the virtual environment. Install python3-venv and try again.' >&2
        exit 1
    fi
fi

printf '%s\n' 'Installing Piper in the local virtual environment...'
"${venv_dir}/bin/python" -m pip install --upgrade pip
"${venv_dir}/bin/python" -m pip install piper-tts

mkdir -p -- "${voice_dir}"
printf 'Downloading voice model %s...\n' "${voice_name}"
"${venv_dir}/bin/python" -m piper.download_voices \
    --data-dir "${voice_dir}" \
    "${voice_name}"

printf 'VOICE_NAME=%s\n' "${voice_name}" > "${config_file}"
printf 'Setup complete. Lesson language: %s. Voice: %s\n' "${lesson_language}" "${voice_name}"
printf '%s\n' 'Test with: ./scripts/speak.sh --text "This is a test."'
printf '%s\n' 'Start the graphical interface with: ./scripts/start-gui.sh'
