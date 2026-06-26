.DEFAULT_GOAL := check
.PHONY: __repository-make-authority build check contract-test lint root-test test verify
.SECONDEXPANSION:

ifeq ($(origin PYTHON),undefined)
override PYTHON := /usr/bin/python3
else
override PYTHON := $(value PYTHON)
endif
export PYTHON
override REPOSITORY_MAKE_DOLLAR := $$
override REPOSITORY_MAKE_OPEN := (
ifneq ($(findstring $(REPOSITORY_MAKE_DOLLAR)$(REPOSITORY_MAKE_OPEN),$(value PYTHON)),)
$(error PYTHON must be a literal executable path, not Make syntax)
endif
ifneq ($(findstring $(REPOSITORY_MAKE_DOLLAR){,$(value PYTHON)),)
$(error PYTHON must be a literal executable path, not Make syntax)
endif
override SHELL := /bin/sh
override .SHELLFLAGS := -c
build check contract-test lint root-test test verify __repository-make-authority: override SHELL := /bin/sh
build check contract-test lint root-test test verify __repository-make-authority: override .SHELLFLAGS := -c

ifneq ($(filter command line,$(origin MAKEFLAGS)),)
$(error MAKEFLAGS must not be overridden for repository verification)
endif
override REPOSITORY_MAKE_FIRST_FLAGS := $(firstword $(MAKEFLAGS))
ifneq ($(filter -%,$(REPOSITORY_MAKE_FIRST_FLAGS)),)
override REPOSITORY_MAKE_FIRST_FLAGS :=
endif
override REPOSITORY_MAKE_SHORT_FLAGS := $(REPOSITORY_MAKE_FIRST_FLAGS) $(filter-out --%,$(filter -%,$(MAKEFLAGS)))
ifneq ($(findstring n,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring t,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring q,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring i,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(filter --just-print --dry-run --recon --touch --question --ignore-errors,$(MAKEFLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override REPOSITORY_MAKEFILE_LIST := $(value MAKEFILE_LIST)
override ROOT := $(shell path='$(subst ','"'"',$(value MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); [ -f "$$path" ] || exit 1; directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile path could not be resolved)
endif
override REPOSITORY_SHELL_LITERAL = $(subst $$,$$$$,$(subst ','"'"',$1))
override REPOSITORY_PARSE_SHELL_LITERAL = $(subst ','"'"',$1)
override REPOSITORY_ROOT_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(ROOT))
override REPOSITORY_PYTHON_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(PYTHON))
override REPOSITORY_PYTHON_IS_VALID := $(shell candidate='$(call REPOSITORY_PARSE_SHELL_LITERAL,$(PYTHON))'; /bin/expr "$$candidate" : '^/' >/dev/null && [ -x "$$candidate" ] && /usr/bin/printf '%s' yes)
ifneq ($(REPOSITORY_PYTHON_IS_VALID),yes)
$(error PYTHON must be an absolute executable path)
endif

build check contract-test lint root-test test verify:: $$(if $$(filter file,$$(origin MAKEFILE_LIST)),,$$(error MAKEFILE_LIST must not be overridden))
build check contract-test lint root-test test verify:: $$(if $$(filter-out $$(REPOSITORY_MAKEFILE_LIST),$$(value MAKEFILE_LIST)),$$(error repository Makefile must be loaded alone))
build check contract-test lint root-test test verify:: $$(if $$(filter-out $$(value MAKEFILE_LIST),$$(REPOSITORY_MAKEFILE_LIST)),$$(error repository Makefile must be loaded alone))
build check contract-test lint root-test test verify:: __repository-make-authority

__repository-make-authority::
	@:

define REPOSITORY_PUBLIC_RECIPES
lint::
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/check_ios_contracts.py'

test:: lint
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_deep_link_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_legacy_build_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_person_profile_image_lifecycle_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_project_path_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_saved_profile_cell_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_saved_profile_model_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_saved_profile_selection_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_saved_profile_write_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_tweet_embed_lifecycle_contract.py'

contract-test::
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_workflow_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_trusted_workflow_contract.py'

build::
	@if [ -x '/usr/bin/xcodebuild' ]; then \
		xcode_major=$$$$('/usr/bin/xcodebuild' -version | /usr/bin/awk 'NR == 1 { split($$$$2, version, "."); print version[1] }'); \
		if [ "$$$$xcode_major" -le 6 ]; then \
			cd '$(REPOSITORY_ROOT_LITERAL)' && '/usr/bin/xcodebuild' -project Twinder.xcodeproj -target Twinder -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO build; \
		else \
			echo "iOS build skipped: this project requires Xcode 6.x for its pre-versioned Swift sources."; \
		fi; \
	else \
		echo "iOS build skipped: xcodebuild is not available on this host."; \
	fi

root-test::
	/bin/sh '$(REPOSITORY_ROOT_LITERAL)/scripts/test-makefile-root.sh'

verify:: root-test lint contract-test test build

check:: verify
endef
$(eval $(REPOSITORY_PUBLIC_RECIPES))
