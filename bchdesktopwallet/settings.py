import os
from pathlib import Path

TRUE_VALUES = ["1", "TRUE", "True", "true"]

debug = os.getenv("ARGOS_DEBUG") in TRUE_VALUES

dev_mode = os.getenv("ARGOS_DEV_MODE") in TRUE_VALUES

home_dir = Path.home()
if "SNAP" in os.environ:
    home_dir = Path(os.environ["SNAP_USER_DATA"])

data_dir = (
    Path(os.getenv("XDG_DATA_HOME", default=home_dir / ".local" / "share"))
    / "argos-translate"
)
os.makedirs(data_dir, exist_ok=True)
