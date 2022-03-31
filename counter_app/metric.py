from prometheus_client import Counter

COUNTER_INCREMENT = Counter('counter_increment', 'Amount of counter increments', ['counter_name'])
COUNTER_RESET = Counter('counter_reset', 'Amount of counter reset', ['counter_name'])
COUNTER_READ = Counter('counter_read', 'Amount of counter reads', ['counter_name'])
