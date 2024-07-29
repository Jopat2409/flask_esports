from flask_esports.utils.decorators import require_int

def test_require_int(app):

    @require_int("test_int", "Incorrect integer value")
    def test_int_return(test_int):
        return test_int

    assert test_int_return(test_int=10) == 10
    assert isinstance(test_int_return(test_int=10), int)

    assert test_int_return(test_int="10") == 10
    assert isinstance(test_int_return(test_int="10"), int)

    with app.app_context():
        response = test_int_return(test_int=10.5).get_json()

    assert response["success"] is False
    assert response["data"]["error-message"] == "Incorrect integer value"

    with app.app_context():
        response = test_int_return(test_int="10.5").get_json()

    assert response["success"] is False
    assert response["data"]["error-message"] == "Incorrect integer value"

    with app.app_context():
        response = test_int_return(test_int="invalid").get_json()

    assert response["success"] is False
    assert response["data"]["error-message"] == "Incorrect integer value"
