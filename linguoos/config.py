import os

VERSION = globals().get("VERSION", "0.1.0")
API_KEY = os.getenv("LINGUO_API_KEY", "dev-key-123")
REQUIRE_API_KEY = os.getenv("LINGUO_REQUIRE_API_KEY", "0") == "1"
