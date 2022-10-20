from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
    def login(self):
        self.client.post("/search", {"sear":"Data Analyst", "location":"Delhi"})

   
    

class AppUser(HttpUser):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
    host="http://localhost:8501/Job_Search"