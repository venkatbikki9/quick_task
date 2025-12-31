##App Port Demo – Docker, Compose & CI

This project is a small web application built mainly to demonstrate Dockerisation, port handling, Docker Compose usage, and a CI pipeline.
The application itself is intentionally simple so that the focus stays on how the app is built, packaged, run, and verified, rather than on business logic.

#Application Overview

The application is a Python Flask service with two endpoints:

1. /
Returns the application name and the port the application believes it is running on.

2. /health
Returns a simple JSON response indicating the application is healthy.

The app reads its listening port from an environment variable (APP_PORT) and exits with an error if the variable is not set.

#Port Configuration and Networking

What port the app listens on and why

The application listens on port 5000.

This port is:

Passed using the environment variable APP_PORT

Used internally by the Flask server inside the container

Why this approach:
Using an environment variable instead of a hardcoded port makes the application flexible and portable. The same image can run in different environments without code changes.

Why the container port and host port are different

Container port: 5000

Host port: 8081

These ports are different by design.

On my system, port 8080 is already used by Jenkins, so using a different host port avoids conflicts. The container continues to use port 5000 internally, while Docker maps it to a free port on the host.

This separation reflects real-world setups where applications should not assume which ports are available on the host machine.
