import os
import tempfile

# Settings are read at import time: force demo mode and a throwaway data dir for tests.
os.environ["DEMO_MODE"] = "1"
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="video-studio-test-")
os.environ.setdefault("FAL_KEY", "")
