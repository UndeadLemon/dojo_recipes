from dojo_recipes import app
from dojo_recipes.controllers import users


if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.