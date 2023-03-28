import os
import pytz
import logging
import traceback
import logging.handlers as handlers

from sys import stderr
from datetime import datetime

class LoggerManager:
    def __init__(
            self,
            name: str | None = ...,
            main_dir_name: str = ...,
            log_dir_name: str | None = ...,
            timezone: str | None = ...,
        ) -> ...:

        # Check params
        if not main_dir_name:
            raise ValueError("Invalid value! Parameter \"main_directory\" can't be null.")
        elif not isinstance(main_dir_name, str):
            raise TypeError("Invalid type! Parameter \"main_directory\" must be \"string\".")
        else:
            self.__main_dir: str = main_dir_name

        # Private Variables
        self.__name: str = name if name is not None else None
        self.__log_dir: str = log_dir_name if log_dir_name is not None else None
        self.__timezone: pytz = pytz.timezone(timezone)


        self.__logger = logging.getLogger(__name__)
        self.__logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [{name}] %(message)s")
        self.__logFormatter.converter = self.convert_time()

    # Display log foramtter level name
    @property
    def __name__(self) -> str:
        return self.__name

    # Display logger main directory
    @property
    def __main_dir__(self) -> str:
        return self.__main_dir
    
    # Display logger specified directories
    @property
    def __log_dir__(self) -> str:
        return self.__log_dir

    # Display logger timezone
    @property
    def __timezone__(self) -> str:
        return self.__timezone

    # Convert logger standard timezone
    def convert_time(self) -> datetime:
        return datetime.now(self.__timezone).timetuple()

    def clear_base_handlers(self) -> None:
        try:
            if self.__logger.hasHandlers():
                self.__logger.handlers.clear()
            self.__logger.setLevel(logging.NOTSET)
        except Exception as error:
            raise f"Unable to clear base logger handlers. "
    
    # Create logger directories
    def create_dirs(self) -> None:
        try:
            if not os.path.exists(os.path.join(os.path.dirname(f"/{self.__main_dir}/logs/"), "logs")):
                os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

            if not os.path.exists(os.path.join(os.path.dirname(f"/{self.__main_dir}/logs/{self.__log_dir}/"), "logs")):
                os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

        except MemoryError | FileNotFoundError | PermissionError | RuntimeError as error:
            raise f"Unable to creatre logger directories. Exception: \"{repr(error)}\". \nTraceback: {traceback.print_stack}"

    # Create loggers
    def create_logger(self) -> logging:

        ch = logging.StreamHandler(stderr)
        ch.setFormatter(logFormatter)
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)

        fh = handlers.TimedRotatingFileHandler(
            os.path.join(os.path.dirname(__file__), "logs", f"{self.__log_dir}.log"),
            when="midnight",
            interval=1,
            backupCount=7,
        )
        fh.setFormatter(logFormatter)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

        mh = MensageiroHandler()
        mh.setFormatter(logFormatterSimples)
        mh.setLevel(logging.INFO)
        logger.addHandler(mh)

        return logger