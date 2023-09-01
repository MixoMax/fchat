#for running commands in the terminal
import os
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))


"""
Script to dockerize the flask app

Directory:

/main.py
/dockerize.py
/LICENSE.md
/README.md
/requirements.txt
/requirements.txt
/data/
    /database.db
/static/
    /css/
        /style.css
    /js/
        /chat.js
/templates/
    /index.html

"""

#check if os is windows or linux
if os.name != "nt":
    raise Exception("This script is only for windows")

def create_DOCKERFILE():
    """Create the DOCKERFILE"""
    #setup the right environment (python >=3.10)
    
    #create the DOCKERFILE
    docker_file_path = "./DOCKERFILE"
    
    #use python 3.10 slim
    docker_strings = [
        "FROM python:3.10-slim\n",
        "WORKDIR /app\n",
        
        "COPY requirements.txt ./\n",
        "COPY main.py ./\n",
        "COPY /data/database.db ./data/\n",
        "COPY /static/css/style.css ./static/css/\n",
        "COPY /static/js/chat.js ./static/js/\n",
        "COPY /templates/index.html ./templates/\n",
        "COPY LICENSE.md ./\n",
        
        "RUN pip install --no-cache-dir --upgrade pip\n",
        "RUN pip install --no-cache-dir -r requirements.txt\n",
        "EXPOSE 80\n",
        "CMD [\"python\", \"main.py\"]\n"
    ]
    
    with open(docker_file_path, "w") as f:
        for s in docker_strings:
            f.write(s)
    
    print("Created DOCKERFILE")

def create_requirements():
    requirements = ["flask", "requests", "flask_sqlalchemy", "dataclasses"]
    with open("./requirements.txt", "w") as f:
        for r in requirements:
            f.write(r + "\n")
    print("Created requirements.txt")

def create_container():
    """Create the docker container"""
    #create the container for DOCKERFILE
    try:
        subprocess.run(["docker", "build", "-t", "chat-app", "-f", "DOCKERFILE", "."], check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
        print("Failed to build container")
        return
    



def run_container():
    """Run the container"""
    #run the container
    os.system("docker run -d -p 80:80 chat-app")
    print("Running container")

def main():
    create_requirements()
    create_DOCKERFILE()
    create_container()
    run_container()

if __name__ == "__main__":
    main()