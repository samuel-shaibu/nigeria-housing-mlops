import pytest
import sys, os

# Get the folder where this file lives (tests/)
current_dir = os.path.dirname(__file__)
# Go back to the project folder
project_root = os.path.join(current_dir, "..")
# Add the root path to Python's search list
sys.path.insert(0, os.path.abspath(project_root))

# Now this import should work
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200