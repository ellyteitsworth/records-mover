__all__ = [
    'Logger',
    'Filterer',
    'LogRecord',
]

from typing import Any, Optional
from .log_record import LogRecord
from .logger import Logger
from .filterer import Filterer


raiseExceptions: bool
CRITICAL: int
FATAL: int
ERROR: int
WARNING: int
WARN: int
INFO: int
DEBUG: int
NOTSET: int


def getLevelName(level: Any): ...


def addLevelName(level: Any, levelName: Any) -> None: ...


def setLogRecordFactory(factory: Any) -> None: ...


def getLogRecordFactory(): ...


def makeLogRecord(dict: Any): ...


class PercentStyle:
    default_format: str = ...
    asctime_format: str = ...
    asctime_search: str = ...
    validation_pattern: Any = ...
    def __init__(self, fmt: Any) -> None: ...
    def usesTime(self): ...
    def validate(self) -> None: ...
    def format(self, record: Any): ...


class StrFormatStyle(PercentStyle):
    default_format: str = ...
    asctime_format: str = ...
    asctime_search: str = ...
    fmt_spec: Any = ...
    field_spec: Any = ...
    def validate(self) -> None: ...


class StringTemplateStyle(PercentStyle):
    default_format: str = ...
    asctime_format: str = ...
    asctime_search: str = ...
    def __init__(self, fmt: Any) -> None: ...
    def usesTime(self): ...
    def validate(self) -> None: ...


BASIC_FORMAT: str


class Formatter:
    converter: Any = ...
    datefmt: Any = ...

    def __init__(
        self,
        fmt: Optional[Any] = ...,
        datefmt: Optional[Any] = ...,
        style: str = ...,
        validate: bool = ...,
    ) -> None: ...

    default_time_format: str = ...
    default_msec_format: str = ...
    def formatTime(self, record: Any, datefmt: Optional[Any] = ...): ...
    def formatException(self, ei: Any): ...
    def usesTime(self): ...
    def formatMessage(self, record: Any): ...
    def formatStack(self, stack_info: Any): ...
    def format(self, record: Any): ...


class BufferingFormatter:
    linefmt: Any = ...
    def __init__(self, linefmt: Optional[Any] = ...) -> None: ...
    def formatHeader(self, records: Any): ...
    def formatFooter(self, records: Any): ...
    def format(self, records: Any): ...


class Filter:
    name: Any = ...
    nlen: Any = ...
    def __init__(self, name: str = ...) -> None: ...
    def filter(self, record: Any): ...


class Handler(Filterer):
    level: Any = ...
    formatter: Any = ...
    def __init__(self, level: Any = ...) -> None: ...
    def get_name(self): ...
    def set_name(self, name: Any) -> None: ...
    name: Any = ...
    lock: Any = ...
    def createLock(self) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def setLevel(self, level: Any) -> None: ...
    def format(self, record: Any): ...
    def emit(self, record: Any) -> None: ...
    def handle(self, record: Any): ...
    def setFormatter(self, fmt: Any) -> None: ...
    def flush(self) -> None: ...
    def close(self) -> None: ...
    def handleError(self, record: Any) -> None: ...


class StreamHandler(Handler):
    terminator: str = ...
    stream: Any = ...
    def __init__(self, stream: Optional[Any] = ...) -> None: ...
    def flush(self) -> None: ...
    def emit(self, record: Any) -> None: ...
    def setStream(self, stream: Any): ...


class FileHandler(StreamHandler):
    baseFilename: Any = ...
    mode: Any = ...
    encoding: Any = ...
    delay: Any = ...
    stream: Any = ...

    def __init__(
        self,
        filename: Any,
        mode: str = ...,
        encoding: Optional[Any] = ...,
        delay: bool = ...,
    ) -> None: ...
    def close(self) -> None: ...
    def emit(self, record: Any) -> None: ...


class _StderrHandler(StreamHandler):
    def __init__(self, level: Any = ...) -> None: ...
    @property
    def stream(self): ...


lastResort: Any


class PlaceHolder:
    loggerMap: Any = ...
    def __init__(self, alogger: Any) -> None: ...
    def append(self, alogger: Any) -> None: ...


def setLoggerClass(klass: Any) -> None: ...


def getLoggerClass(): ...


class Manager:
    root: Any = ...
    disable: int = ...
    emittedNoHandlerWarning: bool = ...
    loggerDict: Any = ...
    loggerClass: Any = ...
    logRecordFactory: Any = ...
    def __init__(self, rootnode: Any) -> None: ...
    def getLogger(self, name: str) -> "Logger": ...
    def setLoggerClass(self, klass: Any) -> None: ...
    def setLogRecordFactory(self, factory: Any) -> None: ...


class RootLogger(Logger):
    def __init__(self, level: Any) -> None: ...
    def __reduce__(self): ...


class LoggerAdapter:
    logger: Any = ...
    extra: Any = ...
    def __init__(self, logger: Any, extra: Any) -> None: ...
    def process(self, msg: Any, kwargs: Any): ...
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def warn(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...

    def exception(
        self, msg: str, *args: Any, exc_info: bool = ..., **kwargs: Any
    ) -> None: ...
    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def log(self, level: Any, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def isEnabledFor(self, level: Any): ...
    def setLevel(self, level: Any) -> None: ...
    def getEffectiveLevel(self): ...
    def hasHandlers(self): ...
    @property
    def manager(self): ...
    @manager.setter
    def manager(self, value: Any) -> None: ...
    @property
    def name(self): ...


def basicConfig(**kwargs: Any) -> None: ...


def getLogger(name: Optional[str] = ...) -> Logger: ...


def critical(msg: str, *args: Any, **kwargs: Any) -> None: ...


fatal = critical


def error(msg: str, *args: Any, **kwargs: Any) -> None: ...


def exception(msg: str, *args: Any, exc_info: bool = ..., **kwargs: Any) -> None: ...


def warning(msg: str, *args: Any, **kwargs: Any) -> None: ...


def warn(msg: str, *args: Any, **kwargs: Any) -> None: ...


def info(msg: str, *args: Any, **kwargs: Any) -> None: ...


def debug(msg: str, *args: Any, **kwargs: Any) -> None: ...


def log(level: Any, msg: str, *args: Any, **kwargs: Any) -> None: ...


def disable(level: Any = ...) -> None: ...


def shutdown(handlerList: Any = ...) -> None: ...


class NullHandler(Handler):
    def handle(self, record: Any) -> None: ...
    def emit(self, record: Any) -> None: ...
    lock: Any = ...
    def createLock(self) -> None: ...


def captureWarnings(capture: Any) -> None: ...
