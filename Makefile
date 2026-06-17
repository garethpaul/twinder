.PHONY: build check contract-test lint test verify

override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3

lint:
	$(PYTHON) "$(ROOT)/scripts/check_ios_contracts.py"

test: lint
	$(PYTHON) "$(ROOT)/scripts/test_saved_profile_selection_contract.py"
	$(PYTHON) "$(ROOT)/scripts/test_saved_profile_write_contract.py"

contract-test:
	$(PYTHON) "$(ROOT)/scripts/test_workflow_contract.py"

build:
	@if command -v xcodebuild >/dev/null 2>&1; then \
		cd "$(ROOT)" && xcodebuild -project Twinder.xcodeproj -target Twinder -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "iOS build skipped: xcodebuild is not available on this host."; \
	fi

verify: lint contract-test test build

check: verify
