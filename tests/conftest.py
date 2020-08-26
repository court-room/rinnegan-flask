from pytest import fixture

from app import celery
from app import factory


@fixture(scope="function")
def test_app():
    app = factory.create_app("testing", celery=celery)
    with app.app_context():
        yield app
