Project Installation Guide
This guide will walk you through the steps to set up and run this project on your local machine.

Prerequisites
Before you begin, ensure you have the following installed:

Git

Python 3

pip (Python package installer)

Installation Steps
Follow these instructions to get your development environment running.

1. Clone the Repository
First, clone the project repository to your local machine using Git.

git clone <your-repository-url>
cd <your-repository-directory>

Note: Replace <your-repository-url> and <your-repository-directory> with the actual URL and project folder name.

2. Create a Virtual Environment
It's recommended to create a virtual environment to manage project-specific dependencies.

python3 -m venv venv

3. Activate the Virtual Environment
Activate the newly created environment. Your terminal prompt should change to indicate that you are now in the virtual environment.

source venv/bin/activate

For Windows, use the command: venv\Scripts\activate

4. Install Dependencies
Install all the required Python packages listed in the requirements.txt file.

pip install -r requirements.txt

5. Run the Application
Start the development server using Uvicorn. The --reload flag will automatically restart the server whenever you make changes to the code.

uvicorn app.main:app --reload

Your application should now be running locally.

(Optional) Process Management with PM2
PM2 is a process manager for Node.js applications, but it can also be used to manage Python applications. This is useful for keeping your application alive in a production environment.

1. Install npm and PM2
First, you need to install npm (Node Package Manager), which comes with Node.js. Then, install PM2 globally.

# For Debian/Ubuntu-based systems
sudo apt update
sudo apt install npm

# Install PM2 globally
npm install pm2 -g

2. Running the App with PM2
You can start your Uvicorn application using PM2.

pm2 start "uvicorn app.main:app" --name my-fastapi-app

You can then manage the process using commands like pm2 list, pm2 stop my-fastapi-app, and pm2 restart my-fastapi-app.