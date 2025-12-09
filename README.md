# Bilabonnement.dk | Internal System

## 📋 Description
This project is developed by Team SAFers for the 3rd semester autumn exam 2025 for IT-Architecture at [Business Academy Copenhagen](https://www.ek.dk/english/exchange/ek-guldbergsgade).

The fictive case presented aims to make a system following a microservice architecture to handle internal processes for Bilabonnement.dk to make them more data driven and effective. The system's architecture has been mapped from an analysis based on models and tools presented in the courses Business- and System Development to which microservices have been created for the following processes: car catalog, damage registration, subscription management, authorization, customer management and support, and employee task management.

The system allows employees at Bilabonnement.dk to have a single source of truth which can easily be integrated into their already existing [customer-orienting system](https://www.bilabonnement.dk) to allow for easy automation and minimizing of redundant tasks.


## 💻 How to Install and Run the Project

### 💾 Git Clone or Download ZIP
First you'll need to have the project in a folder on your PC. If you are familiar with Git, you can simply clone the project. In case you are unfamiliar with Git, you can click "Code" (see image below) and then "Download ZIP". When the .zip file has downloaded, remember to unzip it and place it in at your desired destination.

![alt text](./README_images/git_pull.png)

### 🐳 Docker Desktop
To be able to start the system, you'll need Docker Desktop running. [Click here to download Docker Desktop](https://www.docker.com/products/docker-desktop/).

Your Docker Desktop should look something like this:

![alt_text](./README_images/docker_desktop.png)

### ▶️ Starting the Application
When you've got the project folder unzipped at your desired destination and Docker Desktop running, you can now navigate to your project folder in the command prompt and run `docker compose up --build` like so:

![alt_text](./README_images/cmd_navigation.png)

The system should now be running! 🎉

If the frontend doesn't automatically appear, you should be able to access it on any browser at [http://localhost:8501/](http://localhost:8501/).


## ❓ How to Use
:)

## 🪳 Known Issues
:)

## 📫 Contact
:)
