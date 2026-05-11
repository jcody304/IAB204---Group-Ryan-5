# Main py file used for importing the application factory function, Creating an instance of the Flask App, and Running the development server

# Import the Flask Class (pip install Flask)
from flask import Flask
# Import the create_app function from the travel folder (package). This returns a configured Flask App
from event_management import create_app

# Call the create_app function to create an instance of the Flask Application
app = create_app()

# Condition checks if the file is being run directly (Not imported as a module)
if __name__ == '__main__':
    #Starts the development server
    app.run(debug=True,host='127.0.0.1',port=5001)