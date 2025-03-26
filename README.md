# 🎬 Movies App

A Django web application for managing a list of movies. Users can **add** movies manually with up to three genres (where the primary genre is required, and secondary and third genres are optional) or **generate** a personalized movie recommendation with a single button click. The recommendation system analyzes your movie collection and fetches a highly-rated movie from The Movie Database (TMDb) that matches your dominant genre combination.

Click here to see the demo of the app <br>
<a href="https://www.youtube.com/watch?v=AcFWwOKz7fc" target="_blank">
  <img src="https://img.youtube.com/vi/AcFWwOKz7fc/0.jpg" alt="Watch the video" />
</a>


# 📌 Algorithm Description

The **Movies App** is an intelligent movie management system that not only lets you maintain your collection of favorite films but also provides **tailored movie recommendations** based on your watching habits. The app analyzes each movie’s genres—giving extra weight to the primary genre—to understand your true taste, and then it queries TMDb to find a movie that best matches this dominant combination.

---

## 🧠 How the Algorithm Works

### 1️⃣ Analyzing User Preferences
- The app scans all movies in your database and **counts the genres** used in each movie.
- It gives **extra weight to the primary genre** (the genre you set as most important when adding a movie).
- From this analysis, the app determines your **dominant genre combination**.  
  *Example:*  
  - Movie 1: **Primary:** Animation, **Secondary:** Sci-Fi, **Third:** Horror  
  - Movie 2: **Primary:** Horror, **Secondary:** Drama, **Third:** Comedy  
  - Movie 3: **Primary:** Animation, **Secondary:** Horror, **Third:** Sci-Fi  
  In this case, **Animation** is the most frequent primary genre, and the best pairing comes out as **(Animation, Horror, Sci-Fi)**.

### 2️⃣ Fetching the Best-Matching Movie
- The app **queries TMDb’s API** for highly-rated movies that match your dominant genre combination.
- It **ensures that the primary genre (the one you watch most) is dominant** in the recommended movie.
- It also considers the secondary and third genres, so if your favorites are, say, Animation, Horror, and Sci-Fi, it searches for movies that have all three.
- The algorithm **avoids suggesting movies you’ve already added** to your collection.

### 3️⃣ Displaying the Best Recommendation
- The recommended movie is presented with:
  - **Title**
  - **Release Year**
  - **Genre(s):** (The primary genre is prominently displayed, with secondary and third genres shown only if available.)
  - **IMDb-style Rating**
  - **A Direct Link to its TMDb Page**
  - **A Movie Poster** for a richer, more engaging experience

---

## 🚀 What Makes It Unique?

### Personalized Recommendations
- The app **learns from your movie collection** and suggests films that truly match your taste rather than generic, one-size-fits-all recommendations.

### Dynamic & Real-Time Suggestions
- As you add new movies, the system **updates recommendations instantly**, ensuring your suggestions always reflect your current preferences.

### TMDb-Powered Data
- By fetching live data from TMDb, the app provides **fresh and highly-rated movie suggestions** rather than relying on a static dataset.

### No Duplicates & Smarter Genre Matching
- The algorithm is designed to **avoid recommending movies you've already seen**, ensuring a continuous stream of new and interesting films.
- A **weighted approach** guarantees that your primary genre (your core taste) always takes precedence over secondary influences.

### Simple Yet Powerful
- With an intuitive design, adding movies and viewing recommendations is straightforward—**automating movie discovery** in a fun, efficient way.


---

## 📌 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/GospodinovPetar/movies_app.git
cd movies_app
```

## 2️⃣ Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## 4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 5️⃣ Run the server
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
* If you have already watched the suggestion, click "Add to database" to save it in the database.

# 📌 Future Plans
- Make the logic of the code more readable, easier to understand and follow and overall optimizing the code and the logic
- Add a search bar, enhace fall back logic on the algorithm, when we can't find anything good with the parameters given.

