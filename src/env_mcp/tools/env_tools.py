import re
from pathlib import Path
from typing import Any

# Patterns that indicate a value is a secret — mask these in output
_SECRET_KEYS = re.compile(
    r"(secret|password|passwd|token|key|api_key|private|credential|auth|jwt|cert|seed)",
    re.IGNORECASE,
)
_MASK = "***MASKED***"


def _parse_env_file(path: str) -> dict[str, str]:
    """Parse a .env file into a dict. Handles comments, blank lines, quoted values."""
    result = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        result[key] = value
    return result


def _mask(key: str, value: str) -> str:
    return _MASK if _SECRET_KEYS.search(key) else value


def read_env(path: str, mask_secrets: bool = True) -> dict[str, Any]:
    """Read a .env file and return key-value pairs. Secrets masked by default."""
    try:
        raw = _parse_env_file(path)
        vars_ = {k: (_mask(k, v) if mask_secrets else v) for k, v in raw.items()}
        return {"path": path, "vars": vars_, "count": len(vars_), "error": None}
    except FileNotFoundError:
        return {"path": path, "vars": {}, "count": 0, "error": f"File not found: {path}"}
    except Exception as e:
        return {"path": path, "vars": {}, "count": 0, "error": str(e)}


def validate_env(env_path: str, example_path: str) -> dict[str, Any]:
    """Check env_path against example_path — report missing and extra vars."""
    try:
        actual = _parse_env_file(env_path)
        expected = _parse_env_file(example_path)
        missing = [k for k in expected if k not in actual]
        extra = [k for k in actual if k not in expected]
        empty = [k for k, v in actual.items() if not v and k in expected]
        valid = len(missing) == 0
        return {
            "valid": valid,
            "missing_vars": missing,
            "extra_vars": extra,
            "empty_vars": empty,
            "total_expected": len(expected),
            "total_actual": len(actual),
            "error": None,
        }
    except FileNotFoundError as e:
        return {"valid": False, "missing_vars": [], "extra_vars": [], "empty_vars": [], "error": str(e)}
    except Exception as e:
        return {"valid": False, "missing_vars": [], "extra_vars": [], "empty_vars": [], "error": str(e)}


def diff_envs(path_a: str, path_b: str, mask_secrets: bool = True) -> dict[str, Any]:
    """Compare two .env files — show keys only in A, only in B, and differing values."""
    try:
        a = _parse_env_file(path_a)
        b = _parse_env_file(path_b)
        only_in_a = {k: (_mask(k, a[k]) if mask_secrets else a[k]) for k in a if k not in b}
        only_in_b = {k: (_mask(k, b[k]) if mask_secrets else b[k]) for k in b if k not in a}
        differing = {}
        for k in set(a) & set(b):
            if a[k] != b[k]:
                differing[k] = {
                    "a": _mask(k, a[k]) if mask_secrets else a[k],
                    "b": _mask(k, b[k]) if mask_secrets else b[k],
                }
        return {
            "only_in_a": only_in_a,
            "only_in_b": only_in_b,
            "differing_values": differing,
            "identical_count": len(set(a) & set(b)) - len(differing),
            "error": None,
        }
    except FileNotFoundError as e:
        return {"only_in_a": {}, "only_in_b": {}, "differing_values": {}, "error": str(e)}
    except Exception as e:
        return {"only_in_a": {}, "only_in_b": {}, "differing_values": {}, "error": str(e)}


def list_missing(env_path: str, example_path: str) -> dict[str, Any]:
    """Return only the missing required vars from env_path compared to example_path."""
    result = validate_env(env_path, example_path)
    if result.get("error"):
        return result
    return {
        "missing_vars": result["missing_vars"],
        "count": len(result["missing_vars"]),
        "error": None,
    }
