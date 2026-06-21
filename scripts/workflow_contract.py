CHECKOUT_ACTION = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
SETUP_ACTION = "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405"

REVIEWED_WORKFLOW_LINES = tuple(
    line.rstrip(" \t")
    for line in f"""name: Check
on:
  pull_request:
  push:
    branches:
      - master
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: check-${{{{ github.workflow }}}}-${{{{ github.ref }}}}
  cancel-in-progress: true
jobs:
  check:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.12", "3.14"]
    steps:
      - name: Check out repository
        uses: {CHECKOUT_ACTION} # v6.0.3
        with:
          persist-credentials: false
      - name: Set up Python
        uses: {SETUP_ACTION} # v6.2.0
        with:
          python-version: ${{{{ matrix.python-version }}}}
      - name: Run static contracts
        run: /usr/bin/make check PYTHON=\"$(command -v python)\"""".splitlines()
)


def _significant_lines(workflow):
    return tuple(line.rstrip(" \t") for line in workflow.splitlines() if line.strip())


def validate(workflow):
    if _significant_lines(workflow) == REVIEWED_WORKFLOW_LINES:
        return []
    return ["match the exact reviewed workflow schema and step sequence"]
