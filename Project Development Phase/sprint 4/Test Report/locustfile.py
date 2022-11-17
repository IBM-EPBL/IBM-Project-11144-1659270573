from locust import HttpUser, task
import random
import time
data = ({'user': ' deepansuryarajsv@gmail.com' , 'passw': 'deepan'}, { 'name' : ' yuvankaargilrajsv@gmail.com' , 'passw' : 'yuvan'}, {'user' : ' rajasaro2001@rediffmail.com' , 'passw' : 'deepa'})
post_headers={'Content-Type': 'application/x-www-form-urlencoded'}

class PlasmaDonarUser(HttpUser):
    
    @task(10)
    def login_test(self):
        self.client.get("/requester")
    

    # @task(10)
    # def login_page_test(self):
    #     self.client.post("/loginpage",data=data[random.randint(0,2)], headers=post_headers)

    # @task(20)
    # def stats_test(self):
    #     self.client.get("/stats")

    @task(10)
    def stats_test(self):
        self.client.get("/registration")
    
    @task(20)
    def stats_test(self):
        self.client.get("/requested")