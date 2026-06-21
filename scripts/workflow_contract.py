import re


CHECKOUT_ACTION = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
SETUP_ACTION = "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405"
CHECKOUT_BLOCK = "\n".join((
    "      - name: Check out repository",
    f"        uses: {CHECKOUT_ACTION} # v6.0.3",
    "        with:",
    "          persist-credentials: false",
))
CANONICAL_RUN = '/usr/bin/make check PYTHON="$(command -v python)"'
REVIEWED_STEPS = ["Check out repository", "Set up Python", "Run static contracts"]
FORBIDDEN_EXECUTION_KEYS = {
    "continue-on-error",
    "container",
    "defaults",
    "env",
    "if",
    "shell",
    "working-directory",
}


def _quoted_value(text):
    quote = text[0]
    value = []
    index = 1
    while index < len(text):
        char = text[index]
        if char == quote:
            if quote == "'" and index + 1 < len(text) and text[index + 1] == "'":
                value.append("'")
                index += 2
                continue
            return "".join(value), text[index + 1 :]
        if quote == '"' and char == "\\":
            return None, text
        value.append(char)
        index += 1
    return None, text


def _mapping_entry(line):
    if not line.strip() or line.lstrip().startswith("#") or "\t" in line:
        return None

    indent = len(line) - len(line.lstrip(" "))
    content = line[indent:].rstrip()
    sequence = content.startswith("- ")
    if sequence:
        content = content[2:].lstrip()
    if not content:
        return None

    if content[0] in ("'", '"'):
        key, remainder = _quoted_value(content)
        if key is None or not remainder.lstrip().startswith(":"):
            return indent, "<unsupported-yaml-key>", "", sequence
        value = remainder.lstrip()[1:].strip()
    else:
        match = re.match(r"^([^:#][^:]*?)\s*:(.*)$", content)
        if not match:
            return None
        key = match.group(1).strip()
        value = match.group(2).strip()

    if value.startswith(("'", '"')):
        decoded, remainder = _quoted_value(value)
        if decoded is not None and not remainder.strip():
            value = decoded
    return indent, key, value, sequence


def _mapping_entries(workflow):
    return [entry for line in workflow.splitlines() if (entry := _mapping_entry(line))]


def _direct_mapping(entries, parent_key, parent_indent):
    parents = [index for index, entry in enumerate(entries) if entry[:2] == (parent_indent, parent_key)]
    if len(parents) != 1:
        return None

    children = []
    for indent, key, value, sequence in entries[parents[0] + 1 :]:
        if indent <= parent_indent:
            break
        if indent == parent_indent + 2 and not sequence:
            children.append((key, value))
    return children


def validate(workflow):
    errors = []
    entries = _mapping_entries(workflow)
    actions = re.findall(
        r"^[ \t]*(?:-[ \t]*)?uses:[ \t]*(\S+)(?:[ \t]+#.*)?$",
        workflow,
        re.MULTILINE,
    )

    if len(re.findall(r"^  pull_request:$", workflow, re.MULTILINE)) != 1:
        errors.append("validate pull requests exactly once")
    if "  push:\n    branches:\n      - master" not in workflow:
        errors.append("validate pushes to master")
    if len(re.findall(r"^  workflow_dispatch:$", workflow, re.MULTILINE)) != 1:
        errors.append("allow manual dispatch exactly once")
    permission_declarations = [(indent, sequence) for indent, key, _, sequence in entries if key == "permissions"]
    permissions = _direct_mapping(entries, "permissions", 0)
    if permission_declarations != [(0, False)] or permissions is None:
        errors.append("declare workflow permissions exactly once")
    elif permissions != [("contents", "read")]:
        errors.append("use only read-only contents permission")
    if any(key in FORBIDDEN_EXECUTION_KEYS for _, key, _, _ in entries):
        errors.append("not alter the reviewed workflow execution environment")
    if any(key in {"<<", "<unsupported-yaml-key>"} for _, key, _, _ in entries):
        errors.append("not use unsupported YAML authority constructs")
    if any(value.startswith(("&", "*", "|", ">")) for _, _, value, _ in entries):
        errors.append("not use YAML aliases, anchors, or block scalars")
    if len(re.findall(r"^  cancel-in-progress: true$", workflow, re.MULTILINE)) != 1:
        errors.append("cancel superseded runs exactly once")
    if len(re.findall(r"^    runs-on: ubuntu-24\.04$", workflow, re.MULTILINE)) != 1:
        errors.append("use the fixed Ubuntu runner exactly once")
    if len(re.findall(r"^    timeout-minutes: 10$", workflow, re.MULTILINE)) != 1:
        errors.append("bound the job to ten minutes exactly once")
    if len(re.findall(r"^      fail-fast: false$", workflow, re.MULTILINE)) != 1:
        errors.append("run every supported Python matrix job")
    if len(re.findall(r'^        python-version: \["3\.10", "3\.12", "3\.14"\]$', workflow, re.MULTILINE)) != 1:
        errors.append("test the exact supported Python matrix")
    if CHECKOUT_BLOCK not in workflow:
        errors.append("use the exact credential-free checkout contract")
    if actions != [CHECKOUT_ACTION, SETUP_ACTION]:
        errors.append("use only the reviewed checkout and setup-python actions")
    if workflow.count("persist-credentials:") != 1:
        errors.append("configure checkout credential persistence exactly once")
    if len(re.findall(r"^          python-version: \$\{\{ matrix\.python-version \}\}$", workflow, re.MULTILINE)) != 1:
        errors.append("select the matrix Python version exactly once")
    step_names = [value for indent, key, value, sequence in entries if indent == 6 and sequence and key == "name"]
    if step_names != REVIEWED_STEPS:
        errors.append("use only the three reviewed workflow steps")
    run_commands = [value for indent, key, value, sequence in entries if indent == 8 and not sequence and key == "run"]
    if run_commands != [CANONICAL_RUN]:
        errors.append("run the canonical gate exactly once")
    if "xcodebuild" in workflow:
        errors.append("not imply an unsupported hosted Xcode build")

    return errors
