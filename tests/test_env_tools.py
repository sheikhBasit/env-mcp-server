import pytest
from env_mcp.tools.env_tools import read_env, validate_env, diff_envs, list_missing


@pytest.fixture
def env_file(tmp_path):
    f = tmp_path / ".env"
    f.write_text(
        'DB_HOST=localhost\n'
        'DB_PASSWORD=supersecret\n'
        'API_KEY=abc123\n'
        'APP_NAME=myapp\n'
        'EMPTY_VAR=\n'
    )
    return str(f)


@pytest.fixture
def example_file(tmp_path):
    f = tmp_path / ".env.example"
    f.write_text(
        'DB_HOST=\n'
        'DB_PASSWORD=\n'
        'API_KEY=\n'
        'APP_NAME=\n'
        'REQUIRED_MISSING=\n'
    )
    return str(f)


@pytest.fixture
def env_b(tmp_path):
    f = tmp_path / ".env.prod"
    f.write_text(
        'DB_HOST=prod.db.example.com\n'
        'DB_PASSWORD=prodpass\n'
        'API_KEY=abc123\n'
        'NEW_VAR=only_in_prod\n'
    )
    return str(f)


def test_read_env_masks_secrets(env_file):
    result = read_env(env_file)
    assert result["error"] is None
    assert result["vars"]["DB_HOST"] == "localhost"
    assert result["vars"]["DB_PASSWORD"] == "***MASKED***"
    assert result["vars"]["API_KEY"] == "***MASKED***"
    assert result["vars"]["APP_NAME"] == "myapp"


def test_read_env_no_masking(env_file):
    result = read_env(env_file, mask_secrets=False)
    assert result["vars"]["DB_PASSWORD"] == "supersecret"


def test_read_env_missing_file():
    result = read_env("/nonexistent/.env")
    assert result["error"] is not None
    assert "not found" in result["error"].lower()


def test_validate_env_finds_missing(env_file, example_file):
    result = validate_env(env_file, example_file)
    assert result["error"] is None
    assert result["valid"] is False
    assert "REQUIRED_MISSING" in result["missing_vars"]


def test_validate_env_finds_extra(env_file, example_file):
    result = validate_env(env_file, example_file)
    assert "EMPTY_VAR" in result["extra_vars"]


def test_validate_env_finds_empty(tmp_path):
    # APP_NAME is in both env and example but empty — should be flagged
    env = tmp_path / ".env"
    env.write_text("APP_NAME=\nDB_HOST=localhost\n")
    example = tmp_path / ".env.example"
    example.write_text("APP_NAME=\nDB_HOST=\n")
    result = validate_env(str(env), str(example))
    assert "APP_NAME" in result["empty_vars"]


def test_diff_envs(env_file, env_b):
    result = diff_envs(env_file, env_b)
    assert result["error"] is None
    assert "NEW_VAR" in result["only_in_b"]
    assert "APP_NAME" in result["only_in_a"]
    assert "DB_HOST" in result["differing_values"]


def test_list_missing(env_file, example_file):
    result = list_missing(env_file, example_file)
    assert result["error"] is None
    assert "REQUIRED_MISSING" in result["missing_vars"]
    assert result["count"] == 1
