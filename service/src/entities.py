from enum import Enum


class SessionTypes(Enum):
    FP1 = "FP1"
    FP2 = "FP2"
    FP3 = "FP3"
    SQ = "SQ"
    S = "S"
    Q = "Q"
    R = "R"


class SessionStatus(Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class EventFormat(Enum):
    CONVENTIONAL = "conventional"
    SPRINT = "sprint"


class TireCompounds(Enum):
    SOFT = "SOFT"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    INTERMEDIATE = "INTERMEDIATE"
    WET = "WET"
    UNKNOWN = "UNKNOWN"


class Classification(Enum):
    DNF = "DNF"
    DSQ = "DSQ"
    DNS = "DNS"
    FINISHED = "finished"
