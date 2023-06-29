# TraderAPP
###### powered by

<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM-flattened.png" alt="drawing" width="200"/> <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="drawing" width="200"/><img src="https://www.nginx.com/wp-content/uploads/2018/08/NGINX-logo-rgb-large.png" alt="drawing" width="200"/> 
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Gunicorn_logo_2010.svg/2560px-Gunicorn_logo_2010.svg.png" alt="drawing" width="200"/> <img src="https://raw.githubusercontent.com/tomchristie/uvicorn/master/docs/uvicorn.png" alt="drawing" width="200"/> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/2560px-Amazon_Web_Services_Logo.svg.png" alt="drawing" width="200"/>

## API Documentation
<http://ec2-3-16-255-125.us-east-2.compute.amazonaws.com/docs>

## Architecture
<img src="https://github.com/JuanPChicaC/TraderApp/blob/main/API/sources/documentation/TraderAPP%20AWS%20Architecture.png?raw=true"/>

## Data Desgin
<img src="https://github.com/JuanPChicaC/TraderApp/blob/main/API/sources/documentation/Database%20ER%20diagram.png?raw=true"/>

## Security 
### EC2
<img src="https://github.com/JuanPChicaC/TraderApp/blob/main/API/sources/documentation/ec2_security_group.png?raw=true"/>

### DynamoDB
<img src="https://github.com/JuanPChicaC/TraderApp/blob/main/API/sources/documentation/dynamodb_subnet_group.png?raw=true"/>

## Budget Control
<img src="https://github.com/JuanPChicaC/TraderApp/blob/main/API/sources/documentation/aws_budget.png?raw=true"/>

## Deploy
### Server Setup
1. update the packages list 
    ```sh
    sudo yum update
    ```
2. install git to clone the repository
    ```sh
    sudo yum install git -y
    ```
3. download viertualenv package to create an enviroment for api execution
- Check if python is already installed in the server
    ```sh
    which python3
    ```
- in case that the server doesn´t have python or pip installed, install it.
    ```sh
    sudo yum install python3
    sudo yum install python3-pip
    ```
- once python been installed, download viertualenv module
    ```sh
    python3 -m pip install --user virtualenv
    ```
- create a virtual environment with python 3.9.16 version
    ```sh
    virtualenv venv --python=python3.9.16
    ```
4. install nginx, it will be the server that will receive the http calls
    ```sh
    sudo yum install nginx
    ```
### NGINX setup
1. create the configuration file 
    ```sh
    sudo vim /etc/nginx/sites-enabled/fastapi_nginx
    ```
2. set the configuration
    ```sh
    server {
        listen 80;
        server_name <aws ec2 public ip>;
        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }
    ```
### TraderApp deploy
1. clone the github repository
    ```sh
    git clone https://github.com/JuanPChicaC/TraderApp
    ```
2. activate virtual env
    ```sh
    source venv/bin/activate
    ```
3. install the python packages
    ```sh
    python3 -m pip install -r TraderApp/requirements.txt
    ```
4. install gunicorn
    ```sh
    python3 -m pip install "uvicorn[standard]" gunicorn
    ```
5. set environment variables
    ```sh
    export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
    export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
    export REGION_NAME=<AWS_REGION_NAME>
    export INFORMATION_SERVICE_URL=https://api.polygon.io
    export INFORMATION_SERVICE_KEY=<POLYGON_API_KEY>
    ```
6. execute the main.py file from th API folder
    ```sh
    gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
    ```
