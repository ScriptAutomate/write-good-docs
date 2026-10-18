"""Load tidyfeed settings.

The API token is read from the TIDYFEED_TOKEN environment variable first.
If that is unset, it is read from the `token` key in the config file.
The config file defaults to ~/.config/tidyfeed/config.toml and can be
overridden with --config.

Tokens are created and revoked in the Tidyfeed web app under
Settings > API tokens (https://app.tidyfeed.example/settings/tokens).
Creating a new token does not revoke the old one; both work until the
old one is revoked there. `tidyfeed check-token` calls GET /me to
confirm the active token is accepted.
"""
import os
import tomllib
from pathlib import Path

DEFAULT_CONFIG = Path.home() / ".config" / "tidyfeed" / "config.toml"
API_URL = "https://api.tidyfeed.example/v2"


class ConfigError(Exception):
    pass


def load(config_path=None):
    path = Path(config_path) if config_path else DEFAULT_CONFIG
    data = {}
    if path.exists():
        with open(path, "rb") as f:
            data = tomllib.load(f)
    token = os.environ.get("TIDYFEED_TOKEN") or data.get("token")
    if not token:
        raise ConfigError(
            "no API token: set TIDYFEED_TOKEN or add `token = \"...\"` to " + str(path)
        )
    return {
        "token": token,
        "feeds": data.get("feeds", []),
        "api_url": data.get("api_url", API_URL),
    }
