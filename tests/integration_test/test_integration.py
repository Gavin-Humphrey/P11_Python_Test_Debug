import server
from server import app 


class TestIntegration:
    client = app.test_client()

   
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


    ## Test of booking procedure and club points access
    def test_complete_login_booking_logout_display(self):

        # Test login link
        assert self.client.get('/').status_code == 200

        # Test login showSummary
        response = self.client.post('/showSummary', data={"email":"admin@irontemple.com"})
        assert response.status_code == 200

        # Test booking access
        assert self.client.get(f"/book/{self.competition[0]['name']}/{self.club[0]['name']}").status_code == 200

        # Test booking
        response = self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"],
                "places": 1
            }
        )
        data = response.data.decode()
        success_message = "Great-booking complete!" 
        assert response.status_code == 200
        assert success_message in data

        # Test logout
        assert self.client.get('/logout').status_code == 302

        # Test display club points
        assert self.client.get("/display_board").status_code == 200
        data = data = self.client.get("/display_board").data.decode()
        assert f'{self.club[0]["name"]}' in data
        assert f'<td style="border: 2px solid rgb(163, 34, 42)">{self.club[0]["points"]}</td>' in data
