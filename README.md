```markdown
# OSRS Player Comparison

## Overview

The OSRS Player Comparison is a web application built with Flask that allows users to compare Old School RuneScape (OSRS) players' stats. Users can input player names and get a detailed comparison of their skills and activities.

## Features

- Compare multiple OSRS players' skills and activities.
- Highlight top 4 skill levels and scores. NOTE: NEEDS TO BE FIXED
- Indicate players with level 99 skills with a green star.
- Provide tier groups based on total skill levels and monster skill levels.

## Getting Started

### Prerequisites

To run this project locally, you will need to have the following installed:

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Maremoo2/PlayerLookup.git
   cd osrs-player-comparison
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Ensure your Flask app is set to run correctly. In `app.py`, make sure the following lines are included:

   ```python
   if __name__ == "__main__":
       app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
   ```

2. Start the Flask application:

   ```bash
   python app.py
   ```

3. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

### Deployment

To deploy this application using Render, follow these steps:

1. **Create a `Procfile`** in the root directory of your project with the following content:

   ```
   web: gunicorn app:app
   ```

2. **Ensure `gunicorn` is listed in your `requirements.txt`**:

   ```
   Flask==2.0.2
   requests==2.26.0
   gunicorn==20.1.0
   ```

3. **Create a new web service on Render**:
   - Sign up or log in to Render at [https://render.com/](https://render.com/).
   - Click the "New" button and select "Web Service".
   - Connect your GitHub, GitLab, or Bitbucket repository.
   - Select your repository and branch.
   - Set the build command to:
     ```plaintext
     pip install -r requirements.txt
     ```
   - Set the start command to:
     ```plaintext
     gunicorn app:app
     ```
   - Click "Create Web Service".

4. **Access Your App**: Once deployed, Render will provide you with a URL where your Flask app is hosted. Share this URL with others to let them access your application.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- Thanks to the Flask framework for providing an easy way to build web applications in Python.
- Thanks to the OSRS community for the game and the APIs that make this application possible.
```

### Notes:
- Make sure to update any specific instructions or details that pertain to your project.
- Add any additional sections if necessary, such as "Known Issues" or "Future Work".

-------------------------- ##IMPROVEMENTS-------------------------------
##Improving code quality involves several aspects, including readability, maintainability, performance, security, and scalability. Here are some suggestions to improve your Flask application code:

### 1. Code Structure and Organization
- **Modularize the Code**: Break down the `app.py` into multiple modules to separate concerns, such as routes, models, services, and utilities.
- **Blueprints**: Use Flask Blueprints to organize your routes, especially if your application grows larger.

### 2. Error Handling
- **Graceful Error Handling**: Implement error handling for API calls and other operations to ensure the application can handle unexpected issues gracefully.
- **Custom Error Pages**: Create custom error pages for common HTTP errors like 404, 500, etc.

### 3. Security
- **Input Validation**: Ensure all inputs are validated to prevent injection attacks.
- **Secure Configuration**: Use environment variables to manage sensitive configurations (e.g., API keys) instead of hardcoding them.

### 4. Performance
- **Caching**: Implement caching for frequent API calls or computations to improve performance.
- **Asynchronous Tasks**: For long-running tasks, consider using asynchronous task queues like Celery.

### 5. Testing
- **Unit Tests**: Write unit tests for your functions and routes to ensure your code works as expected.
- **Integration Tests**: Test the integration between different parts of your application.

### 6. Documentation
- **Docstrings**: Add docstrings to your functions and classes to explain what they do.
- **Inline Comments**: Use inline comments where necessary to explain complex logic.

### Example Improvements
Here are specific improvements to your current codebase based on the provided snippets:

#### 1. Modularize the Code
- **app/__init__.py**: Initialize the Flask app.
- **app/routes.py**: Define the routes.
- **app/services.py**: Define functions for fetching and processing player data.
- **app/utils.py**: Utility functions if needed.

##### Example: `app/__init__.py`
```python
from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
```

##### Example: `app/routes.py`
```python
from flask import Blueprint, render_template, request
from .services import get_player_data, compare_players

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def compare_players_route():
    if request.method == "POST":
        player_names = [request.form[key] for key in request.form.keys() if key.startswith("player") and request.form[key]]
        comparison_type = request.form.get("comparison_type")
        skill_filters = request.form.getlist("skill_filter")
        activities_type = request.form.getlist("activities_type")

        comparison_data, tier_groups_data = compare_players(player_names, comparison_type, skill_filters, activities_type)
        return render_template("comparison.html", player_names=player_names, data=comparison_data, tier_groups=tier_groups_data)

    return render_template("index.html")
```

##### Example: `app/services.py`
```python
import requests

def get_player_data(player_name):
    url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.json?player={player_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for skill in data['skills']:
            if skill['level'] == -1:
                skill['level'] = 0
        for activity in data['activities']:
            if activity['score'] == -1:
                activity['score'] = 0
        return data
    return None

def compare_players(player_names, comparison_type, skill_filters, activities_type):
    player_data_list = [get_player_data(name) for name in player_names]
    player_data_list = [data for data in player_data_list if data is not None]

    # ... (rest of the comparison logic) ...

    return comparison_data, tier_groups_data
```

#### 2. Error Handling
Add error handling for the `get_player_data` function and other critical parts of your application.

##### Example: Improved `get_player_data` with Error Handling
```python
import requests

def get_player_data(player_name):
    url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.json?player={player_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for skill in data['skills']:
            if skill['level'] == -1:
                skill['level'] = 0
        for activity in data['activities']:
            if activity['score'] == -1:
                activity['score'] = 0
        return data
    except requests.RequestException as e:
        print(f"Error fetching data for {player_name}: {e}")
        return None
```

#### 3. Custom Error Pages
Create custom error pages for better user experience.

##### Example: `app/routes.py`
```python
@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

#### 4. Caching
Implement caching to reduce redundant API calls.

##### Example: Simple Caching with Flask-Caching
```python
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

def create_app():
    app = Flask(__name__)
    cache.init_app(app)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app

@cache.memoize(60)
def get_player_data(player_name):
    # Same function as before
```

### Conclusion
By modularizing the code, improving error handling, adding custom error pages, and implementing caching, you can make your application more maintainable, robust, and performant. Additionally, adding tests and improving documentation will make it easier for others to understand and contribute to your project.
