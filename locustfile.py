import json
import random
import time
from locust import HttpUser, task, between

def read_questions_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = file.readlines()
    return [q.strip() for q in questions]

def save_logs(file_path, question, question_time, response, response_time, latency):
    log_entry = {
        "question": question,
        "question_time": question_time,
        "response": response,
        "response_time": response_time,
        "latency_ms": latency
    }
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

questions_list = read_questions_from_file('questions_list.txt')

class LLMUser(HttpUser):
    wait_time = between(10, 30)

    @task
    def call_llm_api(self):
        url = "url/to/api"
        question = random.choice(questions_list)
        payload = {}
        headers = {}

        question_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        start_time = time.time()
        response = self.client.post(url, json=payload, headers=headers)
        end_time = time.time()
        response_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        latency = (end_time - start_time) * 1000  # latency in milliseconds

        if response.status_code == 200:
            response_json = response.json()
            save_logs("qa_logs.txt", question, question_time, response_json, response_time, latency)
        else:
            save_logs("qa_logs.txt", question, question_time, f"Error: {response.status_code}", response_time, latency)


# Для запуска:
# locust -f locustfile.py --host=http://ip:port --web-port 0000
