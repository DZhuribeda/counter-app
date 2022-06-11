from enum import Enum


class Entities(str, Enum):
    COUNTER = "counter"


class CounterPermissions(str, Enum):
    READ = "read"
    INCREMENT = "increment"
    EDIT = "edit"
    DELETE = "delete"


class CounterRoles(str, Enum):
    READER = "reader"
    WRITER = "writer"
    ADMIN = "admin"


ENTITY_PERMISSIONS = {
    Entities.COUNTER: {
        CounterRoles.READER: [CounterPermissions.READ],
        CounterRoles.WRITER: [CounterPermissions.READ, CounterPermissions.INCREMENT],
        CounterRoles.ADMIN: [
            CounterPermissions.READ,
            CounterPermissions.INCREMENT,
            CounterPermissions.EDIT,
            CounterPermissions.DELETE,
        ],
    },
}

ENTITY_BASE_ROLE = {
    Entities.COUNTER: CounterPermissions.READ,
}
