import logging

from config import PATHS

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    filename=f"{PATHS["logs"]}\\main_module.log",
    encoding="utf-8",
    filemode="w",
)
logger_main_mod = logging.getLogger("main_module")
logger_main_mod.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    pass
