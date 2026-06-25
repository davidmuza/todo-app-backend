import logging


def configure_logging():
    root_looger = logging.getLogger()
    if not root_looger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
    
    logging.getLogger("app").setLevel(logging.INFO)
    
