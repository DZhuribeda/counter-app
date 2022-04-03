import logging
from opentelemetry import trace
import structlog


def trace_processor(logger, log_method, event_dict):
    current_span = trace.get_current_span()
    if current_span != trace.span.INVALID_SPAN and current_span.is_recording():
        event_dict["trace_id"] = str(current_span.context.trace_id & 0xFFFFFFFFFFFFFFFF)
        event_dict["span_id"] = str(current_span.context.span_id)
    return event_dict


def logging_setup(settings):
    log_level = settings.log_level()
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    shared_processors = [
        structlog.stdlib.add_log_level,
        timestamper,
    ]

    processors=[
        trace_processor,
        # Remove _record & _from_structlog.
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]
    
    if settings.log_json():
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(),)


    structlog.configure(
        processors=shared_processors +  [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within
        # structlog.
        foreign_pre_chain=shared_processors,
        # These run on ALL entries after the pre_chain is done.
        processors=processors,
    )

    handler = logging.StreamHandler()
    # Use OUR `ProcessorFormatter` to format all `logging` entries.
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)
