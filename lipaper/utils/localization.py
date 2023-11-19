import re


def _get_string_quotes(string: str) -> list[int]:
    output = []
    for match in re.finditer(r"\"(\\.|[^\"\\])*\"", string):
        output.extend(list(range(match.start(), match.end() + 1)))

    return output


def _has_assignment(string: str, operator: str = "=", quotes: list[int] = None) -> bool:
    if not quotes:
        quotes = _get_string_quotes(string)

    if (index := string.find(operator)) != -1:
        return index not in quotes

    return False


def _parse_string(string: str) -> str:
    output = ""
    for match in re.finditer(r"\"(\\.|[^\"\\])*\"", string):
        output += match.group(0)[1:-1]

    return output


def _parse_assignment(string: str) -> tuple[str, str]:
    match = re.findall(
        r"^\s*([A-Za-z0-9_.]*\w*)\s*=\s*(.*)", string
    )[0]

    return match[0], _parse_string(match[1])


def _parse(lines: list[str], *, ignore_errors: bool = True) -> dict[str, str]:
    values = []
    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue

        if _has_assignment(line):
            values.append(_parse_assignment(line))

        if not _has_assignment(line) and values:
            values[-1] = (
                values[-1][0], values[-1][1] + _parse_string(line)
            )
        if not _has_assignment(line) and not values and not ignore_errors:
            raise SyntaxError("Assignment operator not found!")

    return {key: value for key, value in values}


def loads(path: str, *, ignore_errors: bool = True) -> dict[str, str]:
    with open(path, mode="r", encoding="utf-8") as file:
        return _parse(file.readlines(), ignore_errors=ignore_errors)
