#!/bin/zsh

PROJECT_DIR="/Users/glytxh/Documents/asciiFITS"

# Give Terminal a moment to create the new window, then size it.
osascript <<'APPLESCRIPT' >/dev/null 2>&1
tell application "Terminal"
  activate
  delay 0.15
  set custom title of front window to "SKYBOX"
  set number of columns of front window to 104
  set number of rows of front window to 58
end tell
APPLESCRIPT

cd "$PROJECT_DIR" || exit 1

printf '\033]0;SKYBOX\a'
clear

if [ ! -d ".venv" ]; then
  echo "SKYBOX cannot find its Python environment."
  echo
  echo "Expected:"
  echo "$PROJECT_DIR/.venv"
  echo
  echo "Run this first:"
  echo "cd $PROJECT_DIR"
  echo "python3 -m venv .venv"
  echo "source .venv/bin/activate"
  echo "pip install -r requirements.txt"
  echo
  echo "Press Enter to close."
  read
  exit 1
fi

source .venv/bin/activate

python -m skybox
EXIT_CODE=$?

if [ "$EXIT_CODE" -ne 0 ]; then
  echo
  echo "SKYBOX closed with an error."
  echo "Exit code: $EXIT_CODE"
  echo
  echo "Press Enter to close."
  read
fi

osascript -e 'tell application "Terminal" to close front window' >/dev/null 2>&1
exit 0
