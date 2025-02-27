# 🎬 Movies App

A simple Django web application for managing a list of movies. Users can **add** movies manually or **generate** a movie with a button click.

## 🚀 Features
- ✅ Display a table of movies
- ✅ Add new movies via a form
- ✅ Generate a movie using a predefined function
- ✅ Responsive and modern design with CSS styling

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
* A movie will be added to the list using a predefined function.

# 📌 Future Plans
🚀 In upcoming updates, I plan to implement a smart movie generation algorithm that will:
* Analyze existing movies in the database to understand the user's movie taste.
* Connect to the OMDb API to fetch movies from a larger dataset.
* Suggest a movie that best matches user preferences based on patterns in previously added movies.
* Provide an option for users to rate generated movies to further refine recommendations.
This will transform the "Generate Movie" feature into an intelligent personalized movie suggestion system. Stay tuned! 🎬✨
