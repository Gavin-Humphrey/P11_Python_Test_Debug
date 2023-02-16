import server
from server import app, MAX_PLACES


class TestMax12PointsBooking:
    client = app.test_client()

    """
    GIVEN a connected Client
    WHEN Client tries to make bookings and enteres number of places
    THEN the number of places if compared to the number of available places,
    and number of club points, and number of places already booked
    to make sure it is within allowed number of booking places of max of 12 
    per competition.
    """
   

    client = app.test_client()
    competition = [
        {
            "name": "Test comp",
            "date": "2023-03-13 00:00:00",
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

    places_booked = [
        {
            "competition": "Test comp",
            "booked": [5, "Test club"]
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club
        server.already_booked = self.places_booked

    def test_returns_less_than_twelve(self):
        booked = 5

        response = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked, 
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )
        data = response.data.decode()
        assert response.status_code == 200
        success_message = "Great-booking complete!"
        assert success_message in data
          

    def test_returns_more_than_twelve_per_comp(self):
        booked = 13
        response = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )
        data = response.data.decode()
        assert response.status_code == 200
        assert f"You cannot book more than {MAX_PLACES} places in a single competition." in data


    