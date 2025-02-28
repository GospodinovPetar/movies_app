# 🎬 Movies App

A simple Django web application for managing a list of movies. Users can **add** movies manually or **generate** a movie with a button click.

![Photo of the App](https://media.discordapp.net/attachments/1242189564089466930/1345103630193266688/image.png?ex=67c354e0&is=67c20360&hm=cc0e7d390a34331132d418e38b1bb011cd985e7764939ed8b1f288cd10e9adfc&=&format=webp&quality=lossless&width=2552&height=1302)

# 📌 Algorithm Description & Why Movies App is Unique  

The **Movies App** is an intelligent movie management system that allows users to store their **favorite films** and receive **personalized movie recommendations** based on their preferences. Unlike traditional static movie lists, this app **dynamically fetches recommendations from The Movie Database (TMDb)** and adapts based on the user's favorite genres.

---

## 🧠 How the Algorithm Works  

### 1️⃣ **Analyzing User Preferences**  
- The app **counts the genres** of all movies in the database.  
- The **most frequently watched genre** is set as the **leading genre**.  
- If a **second genre** exists, it is also considered to generate more relevant recommendations. (e.g If there are three movies (Horror, Horror, Comedy) the recommended movie would be a horror comedy)

### 2️⃣ **Fetching the Best-Matching Movie**  
- The app **queries TMDb's API** for **highly-rated movies** that match the identified genres.  
- It **ensures the leading genre is dominant** in the recommended movie.  
- The algorithm **avoids recommending movies that the user has already added** to prevent duplicates.  

### 3️⃣ **Displaying the Best Recommendation**  
- The selected movie is presented with:  
  - **Title**  
  - **Release year**  
  - **Genre(s)**  
  - **IMDb-style rating**  
  - **A direct link to its TMDb page**  
  - **A movie poster for an enhanced user experience**  

---

## 🚀 What Makes It Unique?  

### **Personalized Recommendations**  
- The app **learns from the user’s preferences** and suggests **truly relevant films** instead of random recommendations.  

### **Dynamic & Real-Time Suggestions**  
- The system **updates recommendations instantly** whenever a new movie is added to the user's favorites.  

### **TMDb-Powered Data**  
- Instead of relying on a static dataset, the app **fetches fresh and highly-rated movies from TMDb**, ensuring **relevant suggestions**.  

### **No Duplicates & Smarter Genre Matching**  
- The algorithm ensures **already-watched movies are not recommended again** and **prioritizes the correct leading genre**.  

### **Simple Yet Powerful**  
- The app **automates movie discovery** without requiring users to manually search for recommendations.  

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
Algorithm not working as intended
