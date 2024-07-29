from flask_esports.app.response_factory import ResponseFactory

def test_success(app):
    """Test success response

    Args:
        app (_type_): _description_
    """
    with app.app_context():
        response = ResponseFactory.success({"test-data": "hello"}).get_json()
    assert response["success"]
    assert response["data"] == {"test-data": "hello"}

def test_error(app):
    with app.app_context():
        response = ResponseFactory.error("This is a test error").get_json()
    assert not response["success"]
    assert response["data"] == {"error-message": "This is a test error"}

def test_conditional(app):
    with app.app_context():
        response = ResponseFactory.conditional(True, {"test-data": "hello"}, "This message should not be shown").get_json()
    assert response["success"]
    assert "error-message" not in response["data"]
    assert response["data"] == {"test-data": "hello"}

    with app.app_context():
        response = ResponseFactory.conditional(False, {"test-data": "hello"}, "This message should be shown").get_json()
    assert not response["success"]
    assert "error-message" in response["data"]
    assert response["data"] == {"error-message": "This message should be shown"}

    with app.app_context():
        response = ResponseFactory.conditional([], {"test-data", "test"}, "Error message").get_json()
    assert not response["success"]
    assert "error-message" in response["data"]
    assert response["data"] == {"error-message": "Error message"}

    with app.app_context():
        response = ResponseFactory.conditional(None, {"test-data", "test"}, "Error message").get_json()
    assert not response["success"]
    assert "error-message" in response["data"]
    assert response["data"] == {"error-message": "Error message"}

    with app.app_context():
        response = ResponseFactory.conditional({}, {"test-data", "test"}, "Error message").get_json()
    assert not response["success"]
    assert "error-message" in response["data"]
    assert response["data"] == {"error-message": "Error message"}

    with app.app_context():
        response = ResponseFactory.conditional("", {"test-data", "test"}, "Error message").get_json()
    assert not response["success"]
    assert "error-message" in response["data"]
    assert response["data"] == {"error-message": "Error message"}
