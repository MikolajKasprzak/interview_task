# interview_task
Project contains: 
- Specialized software application.py
- Python script run.py (works in python 2.7 and python 3.9 environment) that will run application.py and generate artifacts in persistence volume.
- Docker images for each of python version 2.7 and 3.9
- Helm chart with create Cron Job that create pod and necessary volumes

Configuration file is in interview_task/project_verifier/values.yaml where is possible to configure: how often run application, select nodes etc.

## Possible improvements:
- Create additional container that will fetch results from application and upload it on (for example) to block storage or artifactory.
- Describe chart in Chart.yml
- Make proper documentation of script run.py

## Tech
Solution use following technologies:
- Kubernetes 1.22 (tested on Minikube version 1.24)
- Docker
- Helm 3.x

## Requirements:
- K8s cluster with at least one worker node (for example minikube)

## Usage
- Build docker images
```sh
docker build -t project_verifier:python2 -f project_verifier_app/DockerfilePython2 ./project_verifier_app/
docker build -t project_verifier:python3 -f project_verifier_app/DockerfilePython3 ./project_verifier_app/
```
- Push images to Kubernetes repository, example for minikube
```sh
minikube image load project_verifier:python2
minikube image load project_verifier:python3
```
- Configure deployment: Names, How often run application etc
```sh
./project_verifier/values.yaml
```
- Deploy application using helm chart
```sh
helm install <name> ./project_verifier
```
- Delete application 
WARNING it will delete persitance volume that contains results
```sh
helm delete <name>
```

## Example output
Application create for every run folder with following convention YYMMDDHHMMSS_py{version of python like 2 or 3} and two files stdout.txt and version.txt.
The folder will be created in persistance volume.

stdout.txt content
```sh
2021-11-08T18:03:01.334252+01:00
```
version.txt content
```sh
Python 2.7.18
```