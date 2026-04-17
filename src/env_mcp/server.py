from fastmcp import FastMCP
from env_mcp.tools.env_tools import read_env, validate_env, diff_envs, list_missing

mcp = FastMCP("env-mcp-server")


@mcp.tool()
def read(path: str, mask_secrets: bool = True) -> dict:
    """Read a .env file and return all key-value pairs. Secrets are masked by default."""
    return read_env(path, mask_secrets)


@mcp.tool()
def validate(env_path: str, example_path: str) -> dict:
    """Validate a .env file against a .env.example — show missing, extra, and empty vars."""
    return validate_env(env_path, example_path)


@mcp.tool()
def diff(path_a: str, path_b: str, mask_secrets: bool = True) -> dict:
    """Compare two .env files — show keys only in each and differing values."""
    return diff_envs(path_a, path_b, mask_secrets)


@mcp.tool()
def missing(env_path: str, example_path: str) -> dict:
    """List vars required by .env.example that are missing from the .env file."""
    return list_missing(env_path, example_path)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
