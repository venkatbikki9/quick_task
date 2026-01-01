
# App Port Demo – Docker, Compose & CI

This project is a small web application built mainly to demonstrate Dockerisation, port handling, Docker Compose usage, and a CI pipeline.
The application itself is intentionally simple so that the focus stays on how the app is built, packaged, run, and verified, rather than on business logic.

## Application Overview

The application is a Python Flask service with two endpoints:

1. /
Returns the application name and the port the application believes it is running on.

2. /health
Returns a simple JSON response indicating the application is healthy.

The app reads its listening port from an environment variable (APP_PORT) and exits with an error if the variable is not set.

## Port Configuration and Networking


The application listens on port 5000.

This port is passed using the environment variable APP_PORT

Used internally by the Flask server inside the container

### Why this approach:
Using an environment variable instead of a hardcoded port makes the application flexible and portable. The same image can run in different environments without code changes.

Why the container port and host port are different

Container port: 5000

Host port: 8081

These ports are different by design.

On my system, port 8080 is already used by Jenkins, so using a different host port avoids conflicts. The container continues to use port 5000 internally, while Docker maps it to a free port on the host.

This separation reflects real-world setups where applications should not assume which ports are available on the host machine.

## Trafficflow :

Browser → localhost:8081

        → Docker Compose port mapping

        → Container port 5000
        
        → Flask application

## Docker and Logging

1.The application runs inside a Docker container based on python:3.12-slim

2.he container runs as a non-root user

3.All logs go to stdout/stderr

4.Flask’s default logging is used, which means Startup logs, HTTP access logs, Error messages are all visible using docker logs or in CI logs.

No log files are written inside the container.

## CI Pipeline Explanation

The project uses GitHub Actions for CI.
The pipeline runs automatically on every push to the main branch.

## What each step in the pipeline does

### 1.Checkout source code
Pulls the repository contents into the CI runner so Docker can access the Dockerfile and application files.

### 2.Login to Docker Hub
Authenticates securely using GitHub Secrets. Credentials are never stored in the repository.

### 3.Build Docker image
Builds the Docker image using the Dockerfile in the repository.

### 4.Tag the image
The image is tagged using the format:

dockerhub-username/port-demo-app:latest


### 5.Push the image to Docker Hub
Uploads the image so it can be pulled and run from any machine.

### 6.Verification step
Runs the container and calls the /health endpoint to ensure:

-The container starts correctly

-The application responds as expected

-Port configuration works correctly

## How the image is tagged and pushed

The image is tagged during the build step using:

dockerhub-username/port-demo-app:latest


After tagging, the image is pushed to Docker Hub using docker push.
This makes the image reusable and suitable for deployment or further automation.



## Design Decisions
1. Using port 8081 on the host

Why:
Port 8080 is already in use on my system by Jenkins, so exposing the application on the same port would cause a conflict.

2. Keeping container and host ports different

Why:
This avoids port conflicts and demonstrates a real-world Docker networking scenario, especially when multiple services run on the same host.

3. Using Docker Compose instead of only docker run

Why:
Docker Compose clearly documents port mappings, environment variables, and services in one place, making the setup easier to understand and reproduce.


# Summary

This project demonstrates:

Clear understanding of application vs container vs host ports

Correct Docker and Docker Compose usage

Secure and automated CI pipeline

flowchart LR
    User[User / Browser]

    Host[Host Machine<br/>Port: 8081]

    Compose[Docker Compose]

    Container[Application Container<br/>Flask App<br/>APP_PORT=5000]

    User -->|HTTP request :8081| Host
    Host -->|Port mapping 8081 → 5000| Compose
    Compose -->|Container port 5000| Container


