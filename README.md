# Cloud-native-App

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
