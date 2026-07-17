from datetime import timedelta, datetime
from service.src.entities import (
    Classification,
    SessionStatus,
    SessionTypes,
    EventFormat,
    TireCompounds,
)
from sqlalchemy import (
    Float,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    Interval,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Drivers(Base):
    __tablename__ = "drivers"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(String(3))
    number: Mapped[int] = mapped_column()
    country: Mapped[str] = mapped_column(String(30))

    constructor_seasons: Mapped[list["DriverConstructorSeason"]] = relationship(
        back_populates="driver"
    )
    race_results: Mapped[list["RaceResults"]] = relationship(back_populates="driver")


class Constructors(Base):
    __tablename__ = "constructors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    driver_seasons: Mapped[list["DriverConstructorSeason"]] = relationship(
        back_populates="constructor"
    )
    race_results: Mapped[list["RaceResults"]] = relationship(
        back_populates="constructor"
    )


class DriverConstructorSeason(Base):
    __tablename__ = "driver_constructor_season"
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), primary_key=True)
    constructor_id: Mapped[int] = mapped_column(
        ForeignKey("constructors.id"), primary_key=True
    )
    season: Mapped[int] = mapped_column(
        ForeignKey("season_and_points_system.season"), primary_key=True
    )

    driver: Mapped["Drivers"] = relationship(back_populates="constructor_seasons")
    constructor: Mapped["Constructors"] = relationship(back_populates="driver_seasons")
    season: Mapped["SeasonPoints"] = relationship(back_populates="driver_seasons")


class SeasonPoints(Base):
    __tablename__ = "season_and_points_system"
    season: Mapped[int] = mapped_column(primary_key=True)
    points_system: Mapped[dict] = mapped_column(JSON)

    driver_seasons: Mapped[list["DriverConstructorSeason"]] = relationship(
        back_populates="season"
    )
    events: Mapped[list["Events"]] = relationship(back_populates="season")


class Sessions(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    session_type: Mapped[str] = mapped_column(Enum(SessionTypes))
    status: Mapped[str] = mapped_column(Enum(SessionStatus))

    event: Mapped["Events"] = relationship(back_populates="sessions")
    race_results: Mapped[list["RaceResults"]] = relationship(back_populates="session")
    laps: Mapped[list["Laps"]] = relationship(back_populates="session")
    pit_stops: Mapped[list["PitStops"]] = relationship(back_populates="session")


class Events(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    date: Mapped[datetime] = mapped_column(DateTime)
    round: Mapped[int] = mapped_column(Integer)
    circuit_id: Mapped[int] = mapped_column(ForeignKey("circuits.id"))
    format: Mapped[str] = mapped_column(Enum(EventFormat))
    season: Mapped[int] = mapped_column(ForeignKey("season_and_points_system.season"))
    laps: Mapped[int] = mapped_column(Integer)

    season_ref: Mapped["SeasonPoints"] = relationship(back_populates="events")
    circuit_ref: Mapped["Circuits"] = relationship(back_populates="events")
    sessions: Mapped[list["Sessions"]] = relationship(back_populates="event")


class Circuits(Base):
    __tablename__ = "circuits"
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(50))
    distance: Mapped[float] = mapped_column(Float)
    turns: Mapped[int] = mapped_column(Integer)

    events: Mapped[list["Events"]] = relationship(back_populates="circuit_ref")


class RaceResults(Base):
    __tablename__ = "race_results"
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), primary_key=True)
    constructor_id: Mapped[int] = mapped_column(ForeignKey("constructors.id"))
    starting_position: Mapped[int] = mapped_column(Integer)
    finishing_position: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Enum(Classification))
    points: Mapped[int] = mapped_column(Integer)
    gap_to_race_winner: Mapped[timedelta] = mapped_column(Interval)

    session: Mapped["Sessions"] = relationship(back_populates="race_results")
    driver: Mapped["Drivers"] = relationship(back_populates="race_results")
    constructor: Mapped["Constructors"] = relationship(back_populates="race_results")


class Laps(Base):
    __tablename__ = "laps"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    lap_number: Mapped[int] = mapped_column(Integer)
    lap_time: Mapped[timedelta] = mapped_column(Interval)
    sector1_time: Mapped[timedelta] = mapped_column(Interval)
    sector2_time: Mapped[timedelta] = mapped_column(Interval)
    sector3_time: Mapped[timedelta] = mapped_column(Interval)
    tire_compound: Mapped[str] = mapped_column(Enum(TireCompounds))
    stint_number: Mapped[int] = mapped_column(Integer)

    session: Mapped["Sessions"] = relationship(back_populates="laps")
    driver: Mapped["Drivers"] = relationship(back_populates="laps")


class PitStops(Base):
    __tablename__ = "pit_stops"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    lap_number: Mapped[int] = mapped_column(Integer)
    stationary_time: Mapped[timedelta] = mapped_column(Interval)
    total_time: Mapped[timedelta] = mapped_column(Interval)

    session: Mapped["Sessions"] = relationship(back_populates="pit_stops")
    driver: Mapped["Drivers"] = relationship(back_populates="pit_stops")
