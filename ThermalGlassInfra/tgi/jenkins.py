# tgi/jenkins.py
from flask import Flask, request
import requests
import os
import json

class JenkinsHandler:
    def __init__(self, config_file):
        self.app = Flask(__name__)
        self.load_config(config_file)
        self.setup_routes()

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def setup_routes(self):
        @self.app.route('/jenkins_notification', methods=['POST'])
        def handle_notification():
            print("Notification received!")
            data = request.get_json()
            self.process_notification(data)
            return 'OK'

    def process_notification(self, data):
        job_name = data.get('projectName')
        build_url = data.get('buildUrl')
        status = data.get('event')

        if build_url:
            build_number = self.extract_build_number(build_url)

        if status == 'success':
            self.handle_success(job_name, build_number)

    def extract_build_number(self, build_url):
        return build_url.split("/")[-2]  # Get the second-to-last part of the URL

    def handle_success(self, job_name, build_number):
        print(f"Job '{job_name}' (build #{build_number}) completed successfully!")
        file_url = self.build_file_url(job_name)
        local_file_path = self.get_local_file_path()
        self.download_file(file_url, local_file_path)

    def build_file_url(self, job_name):
        return f"{self.config['jenkins_base_url']}/job/{job_name}/ws/{self.config['artifact_name']}"

    def get_local_file_path(self):
        current_dir = os.getcwd()
        return os.path.join(current_dir, self.config['artifact_name'])

    def download_file(self, file_url, local_file_path):
        response = requests.get(file_url)
        if response.status_code == 200:
            self.save_file(response.content, local_file_path)
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")

    def save_file(self, content, local_file_path):
        with open(local_file_path, 'wb') as f:
            f.write(content)
        print(f"File downloaded successfully and saved to {local_file_path}")

    def run(self):
        self.app.run(host=self.config['host'], port=self.config['port'])

if __name__ == '__main__':
    jenkins_handler = JenkinsHandler('config.json')
    jenkins_handler.run()
