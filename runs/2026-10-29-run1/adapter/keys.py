"""Load API keys from the private env file without ever printing them."""
from pathlib import Path

ALIASES = {"OPEN_AI_API_KEY": "OPENAI_API_KEY"}


def load(path=Path.home() / ".config/epistemic-empathy/api-keys.env"):
    keys = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = ALIASES.get(name.strip(), name.strip())
        keys[name] = value.strip().strip('"').strip("'")
    return keys
