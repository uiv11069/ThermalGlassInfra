import ThermalGlassInfra.tgi as tgi
import os


@tgi.on_jenkins_build
def deploy_to_test_board(build_job: tgi.jenkins.build_job):
	print("Notification received!")
	

	if build_job.is_successful():
		print("Build was successful!")
		print(f"Job '{build_job.name}' (build #{build_job.number}) completed successfully!")
	
		# downlaod
		artifact = build_job.download_artifacts(os.getcwd())
          
		# Flash / upload to device
		tgi.adb.upload(artifact)


		tgi.adb.run_command("reboot")
          

		tgi.adb.run_command("python3 run_tests.py")








from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route('/jenkins_notification', methods=['POST'])
def handle_notification():
    print("Notification received!")
    data = request.get_json()

    job_name = data.get('projectName')
    build_url = data.get('buildUrl')
    status = data.get('event')

    # Extract build number from build URL
    if build_url:
        build_number = build_url.split("/")[-2]  # Get the second-to-last part of the URL

    if status == 'success':
        print(f"Job '{job_name}' (build #{build_number}) completed successfully!")

        # URL to the file on Jenkins
        file_url = f"http://192.168.11.147:8080/job/{job_name}/ws/something.txt"

        # Get current working directory
        current_dir = os.getcwd()

        # Path to save the file locally in the current directory
        local_file_path = os.path.join(current_dir, "something.txt")

        # Download the file
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully and saved to {local_file_path}")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")

    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)