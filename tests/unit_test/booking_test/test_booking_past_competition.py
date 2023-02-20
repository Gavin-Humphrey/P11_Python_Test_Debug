import server
from server import app


class TestBookingPastCompetition:
    client = app.test_client()

    """
    GIVEN a connected Client
    WHEN Client tries to make bookings and selects a competition
    THEN the acceptance of the selected competition is verified whether past or future,
    based on the date of the event.
    """
   

    client = app.test_client()
    competitions = [
        {
            "name": "Test_open",
            "date": "2023-03-13 00:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Test_over",
            "date": "2020-03-13 00:00:00",
            "numberOfPlaces": "25"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test_club@email.com",
            "points": "20"
        }
    ]

    @classmethod
    def setup_method(cls):
        server.competitions = cls.competitions
        server.clubs = cls.club



    def test_returns_is_not_over_and_can_be_booked(self):
        response = self.client.get(
            f"/book/{self.competitions[0]['name']}/{self.club[0]['name']}"
        )
        assert response.status_code == 200
     

    def test_returns_is_over_and_cannot_be_booked(self):
        response = self.client.get(
            f"/book/{self.competitions[1]['name']}/{self.club[0]['name']}"
        )
        expected_response = b"The Test_over competition is over and cannot be booked!"
        assert response.status_code == 200
        expected_response in response.data

    