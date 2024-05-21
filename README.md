```markdown
# OSRS Player Comparison

## Overview

The OSRS Player Comparison is a web application built with Flask that allows users to compare Old School RuneScape (OSRS) players' stats. Users can input player names and get a detailed comparison of their skills and activities.

## Features

- Compare multiple OSRS players' skills and activities.
- Highlight top 4 skill levels and scores.
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
   git clone https://github.com/your-username/osrs-player-comparison.git
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
- Replace `https://github.com/your-username/osrs-player-comparison.git` with the actual URL of your GitHub repository.
- Make sure to update any specific instructions or details that pertain to your project.
- Add any additional sections if necessary, such as "Known Issues" or "Future Work".
