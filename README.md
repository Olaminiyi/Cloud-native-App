# Cloud-native-App
- You will need to have the following tools for this project
      - An IDE prefarably Visual Studio Code (VSCode)
      - python3
      - pip3
      - An Iam role with a programmatic access configured on the system (i.e using aws configure)
      - eksctl: for creating kubernetes cluster
      - kubeclt: for intereacting with cluster from our IDE
      - Docker desktop app
      - install other dependencies in the requirement.txt with: pip3 install requirement.txt


### we need to create a new virtual environment using phyton 3 because my current macos environment is been managed by homebrew

- To create a virtual environment, go to your project’s directory and run the following command. This will create a new virtual environment in a local folder named .venv:

                   python3 -m venv .venv

The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it .venv.

venv will create a virtual Python installation in the .venv folder.
### You should exclude your virtual environment directory from your version control system using .gitignore or similar.

- Activate a virtual environment

                  source .venv/bin/activate

- To confirm the virtual environment is activated, check the location of your Python interpreter:

                   which python

While the virtual environment is active, the above command will output a filepath that includes the .venv directory, by ending with the following:


- installing dependencies

![alt text](images/1.1.png)
![alt text](images/1.2.png)

- run application with python3
                  python3 app.py

- App Running on http://127.0.0.1:5000

![alt text](images/1.3.png)
![alt text](images/1.4.png)


To create  ECR resource on the AWS console with python, we need to  install or update the AWS SDK for Python.

The SDK is composed of two key Python packages: Botocore (the library providing the low-level functionality shared between the Python SDK and the AWS CLI) and Boto3 (the package implementing the Python SDK itself).

- install the latest Boto3 release via pip:
                  pip3 install boto3

![alt text](images/1.9.png)

- install other dependencies like flask and psutils
                  pip3 install psutils==5.8.0
                  pip3 install flask==2.2.3

![alt text](images/1.1.png)
![alt text](images/1.2.png)

### create ecr.py for ecr configurtion file

                import boto3

                ecr_client = boto3.client('ecr')

                repository_name = "my_monitoring_app_image"
                response = ecr_client.create_repository(repositoryName=repository_name)

                repository_uri = response['repository'] ['repositoryUri']
                print(repository_uri)

- run it with:
                  python3 ecr.py

![alt text](images/1.3.png)

- checked the console if the resource was created successfully
![alt text](images/1.4.png)

- create a Dockerfile for the application

 ![alt text](images/1.5.png)

 - build the image, you can check the image on your docker desktop app

 ![alt text](images/1.6.png)
 ![alt text](images/1.7.png)
 
 - run the image to know if the image was built correctly

![alt text](images/1.8.png)
![alt text](images/1.4.png)

- create a file ecr.py for creating Amazon ECR configuration

![alt text](images/1.10.png)

- run the file and check the resource on the aws console

            python3 ecr.py

![alt text](images/1.11.png)
![alt text](images/1.12.png)


- push the image by clicking on "view push push command in ecr repo", push the image with the following commands 

                aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992382761454.dkr.ecr.us-east-1.amazonaws.com

                docker build -t my_monitoring_app_image .

                docker tag my_monitoring_app_image:latest 992382761454.dkr.ecr.us-east-1.amazonaws.com/my_monitoring_app_image:latest

                docker push 992382761454.dkr.ecr.us-east-1.amazonaws.com/my_monitoring_app_image:latest

![alt text](images/1.13.png)
![alt text](images/1.14.png)
![alt text](images/1.15.png)
![alt text](images/1.16.png)

- check if the image was pushed successfully on the aws console

![alt text](images/1.17.png)

### we need to create kubenetes cluster on AWS for our application
- we need to install kubernetes, eksctl to create the cluster and also install kubectl to interact with kubernetes cluster using commmand line interface

            pip3 install kubernetes==10.0.1

![alt text](images/1.20.png)

- we will use eksctl to create the cluster from our CLI

      $ eksctl create cluster \
      --name cloud-Native-App \
      --region us-east-1 \
      --nodegroup-name worker \
      --node-type t2.micro \
      --nodes 3      

![alt text](images/1.18.png)
![alt text](images/1.19.png)

- check the aws for the resource created

![alt text](images/1.21.png)
![alt text](images/1.22.png)

### creating deployment and service for deploying our application on the cluster and accessing the application from the web browser
- the deployment and service are normally created as a manifest files and apply using kubectl command

- we will create our own deployment and service using python
- create  a file called eks.py to containg the deployment and service configuration

                              #create deployment and service
                              from kubernetes import client, config

                              # Load Kubernetes configuration
                              config.load_kube_config()

                              # Create a Kubernetes API client
                              api_client = client.ApiClient()

                              # Define the deployment
                              deployment = client.V1Deployment(
                              metadata=client.V1ObjectMeta(name="my-flask-app"),
                              spec=client.V1DeploymentSpec(
                                    replicas=1,
                                    selector=client.V1LabelSelector(
                                          match_labels={"app": "my-flask-app"}
                                    ),
                                    template=client.V1PodTemplateSpec(
                                          metadata=client.V1ObjectMeta(
                                          labels={"app": "my-flask-app"}
                                          ),
                                          spec=client.V1PodSpec(
                                          containers=[
                                                client.V1Container(
                                                      name="my-flask-container",
                                                      image="992382761454.dkr.ecr.us-east-1.amazonaws.com/my_monitoring_app_image",
                                                      ports=[client.V1ContainerPort(container_port=5000)]
                                                )
                                          ]
                                          )
                                    )
                              )
                              )

                              # Create the deployment
                              api_instance = client.AppsV1Api(api_client)
                              api_instance.create_namespaced_deployment(
                              namespace="default",
                              body=deployment
                              )

                              # Define the service
                              service = client.V1Service(
                              metadata=client.V1ObjectMeta(name="my-flask-service"),
                              spec=client.V1ServiceSpec(
                                    selector={"app": "my-flask-app"},
                                    ports=[client.V1ServicePort(port=5000)]
                              )
                              )

                              # Create the service
                              api_instance = client.CoreV1Api(api_client)
                              api_instance.create_namespaced_service(
                              namespace="default",
                              body=service
                              )

- run the eks.py script to create service and deployment
- check for the pods, deployment and services are created successfully

![alt text](images/1.23.png)


- Expose port 5000 in the security group of the cluster

![alt text](images/1.24.png)
![alt text](images/1.26.png)

- do port forwarding to attached the application port to computer machine port to be able to view the application on the browser

            kubectl port-forward svc/my-flask-service  5000:5000

- check if the app is running from port 5000 on the browser

![alt text](images/1.27.png)
![alt text](images/1.28.png)