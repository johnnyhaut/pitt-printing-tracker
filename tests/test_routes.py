import os
import tempfile
import pytest
from main_app import app, Base, Printer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_client():
    """Temporary DB + logged-in user for easy testing."""

    db_fd, db_path = tempfile.mkstemp()
    test_engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=test_engine)

    TestingSessionLocal = sessionmaker(bind=test_engine)
    db = TestingSessionLocal()

    # Add a sample printer
    sample = Printer(
        printer_location="Hillman",
        printer_type="Color",
        printer_status="Online",
        printer_issue=""
    )
    db.add(sample)
    db.commit()

    global db_session
    db_session = db

    app.config["TESTING"] = True
    client = app.test_client()

    with client.session_transaction() as sess:
        sess["username"] = "brandon"

    yield client

    try:
        os.close(db_fd)
    except:
        pass


def test_login_success(test_client):
    """Checks that logging in redirects correctly."""
    response = test_client.post(
        "/login",
        data={"user": "brandon", "pass": "pitt123"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"map" in response.data.lower()


def test_map_page_loads(test_client):
    """Map page should load successfully."""
    response = test_client.get("/map/")
    assert response.status_code == 200


def test_default_redirects_to_login(test_client):
    """Home page should redirect to the login page."""
    response = test_client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_report_page_loads(test_client):
    """Checks that the report page loads for a valid printer."""
    response = test_client.get("/report/1")
    assert response.status_code == 200
