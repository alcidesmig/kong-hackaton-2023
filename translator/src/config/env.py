import os

CACHE_ENABLED = os.getenv("CACHE") == "True"
LANGUAGE_AUTODETECT_ENABLED = os.getenv("LANGUAGE_AUTODETECT") == "True"
DEFAULT_LANGUAGE_SRC = os.getenv("DEFAULT_LANGUAGE_SRC", "Portuguese")
LANGUAGE_TARGET = os.getenv("LANGUAGE_TARGET", "English")
MAX_PAYLOAD_SIZE = os.getenv("MAX_PAYLOAD_SIZE", 4096)
SERVER_PORT = os.getenv("SERVER_PORT", 25564)
