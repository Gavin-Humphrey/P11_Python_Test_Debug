from locust import HttpUser, task


class GUDLFT(HttpUser):

    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post('/showSummary', data={"email":"admin@irontemple.com"})

    @task
    def book(self):
        self.client.get("/book/Fall Classic/Simply Lift")

    @task
    def purchasePlaces(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 1, 
                "club": "Iron Temple",
                "competition": "Fall Classic"
            }
        )

    @task
    def display_board(self):
        self.client.get("/display_board")


    @task
    def logout(self):
        self.client.get('/logout')