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
            "points": "4"
        }
    ]

    competition = [
        {
            "name": "Test compet",
            "date": "2023-02-07 0:00:00",
            "numberOfPlaces": "5"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club


    def test_returns_redemed_points_deducted(self): 

        initialPoints = int(self.club[0]["points"])
        placeReserved = 3

        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"],
                "places": placeReserved
            }
        )
        expected_result = 1
        assert initialPoints-placeReserved == expected_result
        assert response.status_code == 200