import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app

DB_PATH = "./test.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

for table in Base.metadata.tables.values():
    table.schema = None

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def seed_catalog(db_session):
    from app.models.catalog import (
        EventState,
        OrderStatus,
        PaymentMethod,
        ReservationState,
        TableState,
        TableType,
        TicketState,
        TypeUser,
    )

    if db_session.query(TypeUser).first():
        return

    db_session.add_all(
        [
            TypeUser(id=1, name="cliente"),
            TypeUser(id=2, name="admin"),
            EventState(id=1, name="activo"),
            EventState(id=2, name="cancelado"),
            ReservationState(id=1, name="pendiente"),
            ReservationState(id=2, name="confirmada"),
            TableState(id=1, name="disponible"),
            TableState(id=2, name="reservada"),
            TableType(id=1, name="regular"),
            TableType(id=2, name="vip"),
            TicketState(id=1, name="activo"),
            TicketState(id=2, name="usado"),
            PaymentMethod(id=1, name="efectivo"),
            PaymentMethod(id=2, name="transferencia"),
            OrderStatus(id=1, name="pending"),
            OrderStatus(id=2, name="paid"),
        ]
    )
    db_session.commit()


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)
