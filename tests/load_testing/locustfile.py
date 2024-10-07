from locust import FastHttpUser, task


class WebsiteUser(FastHttpUser):
    # wait_time = between(5, 10)
    insecure = True

    # def on_start(self) -> None:
    #     self.client.post(
    #         "/api/v1/auth/login",
    #         {"username": "vedaka13@yandex.ru", "password": "string"},
    #     )

    # @task
    # def me(self) -> None:
    #     self.client.get("/api/v1/users/me")

    @task
    def products(self) -> None:
        self.client.get("/api/v1/products")
