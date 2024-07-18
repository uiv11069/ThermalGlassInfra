import os
from tgi.jenkins import JenkinsHandler

def main():
    # Construiți calea absolută către config.json
    config_path = os.path.join("/mnt/c/Users/AndreiGhilencea/Desktop/ThermalGlassInfrastructure/ThermalGlassInfra/tgi/config.json")
    jenkins_handler = JenkinsHandler(config_path)
    jenkins_handler.run()

if __name__ == '__main__':
    main()
