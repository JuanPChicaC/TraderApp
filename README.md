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

