# Fleet Management System

This project is a **fleet management system** with a **Flask-based front-end** that interacts with a **Go-based backend API**. The goal of this system is to help manage a fleet of vehicles, including tracking vehicles, managing drivers, handling maintenance schedules, and more. The Flask front-end communicates with the Go API to provide a web interface for users to view and manage fleet data.

## Features

### Go Backend API
- **Manage Fleet Data**: Keep track of vehicles, drivers, trips, and maintenance schedules.
- **RESTful API**: Exposes API endpoints to interact with fleet data.
- **Real-Time Operations**: Perform actions like adding vehicles, assigning drivers, and scheduling maintenance.

### Flask Front-End
- **User Interface**: A web-based interface to display and interact with fleet data.
- **CRUD Operations**: Allows users to create, read, update, and delete fleet-related information.
- **Communication with Go API**: Sends requests to the Go backend to fetch and manipulate data.

## Tech Stack

- **Front-End**: Flask (Python)
- **Back-End**: Go (Golang)
- **Database**: (You can specify the database here, such as MySQL, PostgreSQL, etc.)
- **API Communication**: RESTful APIs (HTTP)

## Prerequisites

- Python 3.x
- Flask
- (Any database you are using, e.g., MySQL, PostgreSQL)

## Installation

### Clone the repository

```bash
git clone https://github.com/sxcntqnt/dayuno
cd dayuno


python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

pip install -r requirements.txt

export FLASK_APP=main.py
export FLASK_ENV=development

flask run

```


### What's New:
- Added Flask environment variable setup (`FLASK_APP` and `FLASK_ENV`).
- Included the `flask run` command to start the Flask server.

Now, the README contains all the necessary steps to run the Flask app, including setting the environment variables and starting the Flask development server. Let me know if this works!

