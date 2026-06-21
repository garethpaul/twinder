#!/usr/bin/env sh
set -eu
PATH=/usr/bin:/bin
export PATH
ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && /bin/pwd -P)
TEMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/twinder-make-authority-XXXXXX")
trap 'rm -rf "$TEMP_ROOT"' EXIT HUP INT TERM
unset MAKEFILES MAKEFILE_LIST MAKEFLAGS MFLAGS MAKEOVERRIDES ROOT SHELL
CONTROL_DIR="$TEMP_ROOT/control"; CHECKOUT="$TEMP_ROOT/twinder app's [gate] \"quoted\" \`touch TWINDER_ROOT_MARKER\`"; ATTACKER_ROOT="$TEMP_ROOT/attacker"; LOG="$TEMP_ROOT/commands.log"; SHELL_LOG="$TEMP_ROOT/shell.log"
mkdir -p "$CONTROL_DIR" "$CHECKOUT/scripts" "$ATTACKER_ROOT"; CONTROL_DIR=$(CDPATH= cd -- "$CONTROL_DIR" && /bin/pwd -P); CHECKOUT=$(CDPATH= cd -- "$CHECKOUT" && /bin/pwd -P); MAKEFILE="$CHECKOUT/Makefile"; cp "$ROOT_DIR/Makefile" "$MAKEFILE"
FAKE_PYTHON="$TEMP_ROOT/trusted-python"
cat >"$FAKE_PYTHON" <<'EOF'
#!/bin/sh
printf '%s|%s|%s\n' "$PWD" "$0" "$*" >> "$TWINDER_COMMAND_LOG"
EOF
chmod +x "$FAKE_PYTHON"
for script in test-makefile-root.sh check_ios_contracts.py test_deep_link_contract.py test_legacy_build_contract.py test_project_path_contract.py test_saved_profile_cell_contract.py test_saved_profile_model_contract.py test_saved_profile_selection_contract.py test_saved_profile_write_contract.py test_workflow_contract.py; do cp "$FAKE_PYTHON" "$CHECKOUT/scripts/$script"; done
FAKE_SHELL="$TEMP_ROOT/fake-shell"; printf '#!/bin/sh\nprintf invoked >> %s\nexec /bin/sh "$@"\n' "'$SHELL_LOG'" >"$FAKE_SHELL"; chmod +x "$FAKE_SHELL"
run_case() { target=$1; mode=$2; rm -f "$LOG" "$SHELL_LOG"; set +e; case "$mode" in default) (cd "$CONTROL_DIR"&&TWINDER_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "$target") >/dev/null 2>&1;; command-root) (cd "$CONTROL_DIR"&&TWINDER_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" ROOT="$ATTACKER_ROOT" "PYTHON=$FAKE_PYTHON" "$target") >/dev/null 2>&1;; environment-root) (cd "$CONTROL_DIR"&&ROOT="$ATTACKER_ROOT" TWINDER_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "$target") >/dev/null 2>&1;; command-shell) (cd "$CONTROL_DIR"&&TWINDER_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" SHELL="$FAKE_SHELL" "PYTHON=$FAKE_PYTHON" "$target") >/dev/null 2>&1;; environment-shell) (cd "$CONTROL_DIR"&&SHELL="$FAKE_SHELL" TWINDER_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "$target") >/dev/null 2>&1;; esac; status=$?; set -e; [ "$status" -eq 0 ]; [ ! -e "$SHELL_LOG" ]; [ "$target" = build ] || grep -Fq "$CHECKOUT" "$LOG"; }
executed=0; for target in build check contract-test lint root-test test verify; do for mode in default command-root environment-root command-shell environment-shell; do run_case "$target" "$mode"; executed=$((executed+1)); done; done; [ "$executed" -eq 35 ]
MARK="$TEMP_ROOT/python-syntax"; BAD="\$(shell /usr/bin/touch '$MARK')"; if (cd "$CONTROL_DIR"&&/usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$BAD" lint) >"$TEMP_ROOT/python.out" 2>&1; then exit 1; fi; [ ! -e "$MARK" ]
if (cd "$CONTROL_DIR"&&/usr/bin/make --no-print-directory -f "$MAKEFILE" MAKEFILE_LIST=/tmp/untrusted check) >"$TEMP_ROOT/list" 2>&1; then exit 1; fi; grep -Fq 'MAKEFILE_LIST must not be overridden' "$TEMP_ROOT/list"
PRE="$TEMP_ROOT/pre.mk"; PRE_MARKER="$TEMP_ROOT/pre-ran"; printf '%s\n' "\$(shell /usr/bin/touch '$PRE_MARKER')" >"$PRE"; if (cd "$CONTROL_DIR"&&MAKEFILES="$PRE" /usr/bin/make --no-print-directory -f "$MAKEFILE" check) >"$TEMP_ROOT/pre" 2>&1; then exit 1; fi; grep -Fq 'MAKEFILES must be empty' "$TEMP_ROOT/pre"; [ -e "$PRE_MARKER" ]
if (cd "$CONTROL_DIR"&&/usr/bin/make --no-print-directory -f "$MAKEFILE" MAKEFLAGS=-n check) >"$TEMP_ROOT/flags" 2>&1; then exit 1; fi; grep -Fq 'MAKEFLAGS must not be overridden' "$TEMP_ROOT/flags"
for flag in -n --just-print --dry-run --recon -t --touch -q --question -i --ignore-errors; do if (cd "$CONTROL_DIR"&&/usr/bin/make "$flag" --no-print-directory -f "$MAKEFILE" check) >"$TEMP_ROOT/flag" 2>&1; then exit 1; fi; grep -Fq 'non-executing or error-ignoring MAKEFLAGS are not supported' "$TEMP_ROOT/flag"; done
printf '%s\n' 'Make authority tests passed: 35 target/authority cases, raw Python syntax, startup, MAKEFLAGS, and 10 mode rejections'
