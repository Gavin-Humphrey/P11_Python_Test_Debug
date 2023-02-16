from server import app


class TestLoginEmail:
    client = app.test_client()
    """
    GIVEN a Client app
    WHEN a Client tries to login
    THEN check the email is valid and not empty
    """

    def test_returns_valid_email(self):
        response = self.client.post('/showSummary', data={"email":"admin@irontemple.com"})
        assert response.status_code == 200

    def test_returns_invalid_email(self):
        response = self.client.post('/showSummary', data={"email":"invalid@email.com"})
        assert response.status_code == 405

    def test_returns_empty_email(self):
        response = self.client.post('/showSummary', data={"email":""})
        assert response.status_code == 405