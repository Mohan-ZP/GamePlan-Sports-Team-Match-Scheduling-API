import logging

logging.basicConfig(
    filename=r"app\logs\gameplan.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("gameplan_logger")
