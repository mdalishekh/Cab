# Project Setup Instructions

# 1. Install VS Code
Download and install Visual Studio Code from the official website:
[https://code.visualstudio.com/download](https://code.visualstudio.com/download)

# 2. Install VS Code
Follow the installation instructions for your operating system to install Visual Studio Code.

# 3. Install Python Extension in VS Code
Once VS Code is installed, open it and install the Python extension. You can do this by:

1. Opening the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window.
2. Searching for "Python" in the search box.
3. Clicking on the "Install" button for the Python extension by Microsoft.

This extension provides rich support for the Python language, including features like IntelliSense, linting, and debugging.

# 4. Install Python Interpreter
Download and install the Python interpreter from the official website:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

Make sure to add Python to your system's PATH during the installation process. This allows you to run Python from the command line or terminal.

# 5. Install Required Packages
After cloning the project repository, navigate to the project directory and run the following command to install all the necessary packages:

```bash
pip install -r requirements.txt
```
# 6. Run this application in VS code terminal using this command
```bash
uvicorn main:app --reload
```

# 7. set PORT as env key in environment variable and it's value should be  8000

# 8. Use this command to deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
Now this project will be started
