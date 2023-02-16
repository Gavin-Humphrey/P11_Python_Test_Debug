import server
from server import app 


class TestBooking:
    client = app.test_client()

    """
    GIVEN a connected Client
    WHEN Client tries to make bookings
    THEN check that the is not zero and 
    is allowed for number of booking places.
    """
    club = [
        {
            "name": "Test club",
            "email": "admin@irontemple.com",
            "points": "2"
        }
    ]

    competition = [
        {
            "name": "Test comp",
            "date": "2023-02-07 0:00:00",
            "numberOfPlaces": "5"
        }
    ]
  
    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    # Club has sufficient points
    def test_returns_has_points_within_allowed(self):
        club_point = int(self.club[0]["points"])
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"],
                "places": 2
            }
        )
        data = response.data.decode()
        success_message = "Great-booking complete!" 
        assert club_point >= 0
        assert response.status_code == 200
        assert success_message in data

    # Club has less points 
    def test_returns_has_less_points_than_allowed(self):
        club_point = int(self.club[0]["points"])
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"],
                "places": 5
            }
        )
        data = response.data.decode()
        error_message = "Isufficient points to book this amount of places."
        assert club_point >= 0
        assert response.status_code == 200
        assert error_message in data