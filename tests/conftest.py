from pytest import fixture

from app import create_app


@fixture(scope="function")
def test_app():
    app = create_app("testing")
    with app.app_context():
        yield app
