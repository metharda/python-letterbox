# Python Letterbox

Python Letterbox is a movie review application inspired by Letterboxd, developed using Python. It enables users to add films, write reviews, and manage a personal movie database.

## Features

- **Add Films**: Users can add new films to their personal database.
- **Write Reviews**: Users can write and store reviews for films.
- **Film Database Management**: Manage and organize a collection of films and associated reviews.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/metharda/python-letterbox.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd python-letterbox
   ```
3. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
4. **Activate the virtual environment**:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On Mac/Linux:
      ```bash
      source venv/bin/activate
      ```
5. **Install required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
6. **Create an .env file and get an API key from https://www.themoviedb.org
### Running the Application

```bash
python main.py
```

## Project Structure

- `main.py`: The main entry point of the application.
- `anaSayfa.py`: Handles the main page functionalities.
- `filmEkle.py`: Module for adding new films.
- `filmListe.py`: Displays the list of films.
- `incelemeEkle.py`: Module for adding reviews.
- `incelemeListe.py`: Displays the list of reviews.
- `veritabani.py`: Handles database operations.
- `database.json`: JSON file where film and review data are stored.
- `assets/`: Directory containing assets such as images or other resources.

## License

This project is licensed under the MIT License.
