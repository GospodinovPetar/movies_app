# 🎬 Movies App

A simple Django web application for managing a list of movies. Users can **add** movies manually or **generate** a movie with a button click.

## 🚀 Features
- ✅ Display a table of movies stored in the database  
- ✅ Add new movies via a form  
- ✅ Generate a **personalized** movie recommendation based on watched movies  
- ✅ Ensure the **most-watched genre is prioritized** when generating movies  
- ✅ Require a **secondary genre (if available)** for more accurate suggestions  
- ✅ Prevent duplicate recommendations by checking existing movies  

---

## 📌 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/GospodinovPetar/movies_app.git
cd movies_app
```

## Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to access the app.

# 📌 Usage

## 🎥 Adding a Movie
* Click the "Add a Movie" button.
* Fill in the movie details.
* Click Done, and the movie will appear in the list.
## 🔄 Generating a Movie
* Click the "Generate Movie" button.
* The system analyzes your most-watched genres and fetches a highly-rated movie from The Movie Database (TMDb).
* The recommended movie will be displayed with a link to its TMDb page.
* If you have already watched the suggestion, click "Add to watched already" to save it in the database.

# 📌 Future Plans
🚀 In upcoming updates, I plan to implement adding multiple genres to the films you watch, primary and secondary and optimizing the algorithm.
