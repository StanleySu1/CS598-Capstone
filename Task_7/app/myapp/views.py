from django.shortcuts import render
import json
import nltk
import numpy as np
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEWS_DIR = os.path.join(BASE_DIR, 'myapp')  # Where your review JSON files live

nltk.download('punkt')
nltk.download('stopwords')

def load_reviews_for_cuisine(cuisine):
    file_path = os.path.join(REVIEWS_DIR, f"{cuisine.lower()}_reviews.json")
    reviews = []
    if not os.path.exists(file_path):
        return reviews
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            reviews.append(json.loads(line))
    return reviews

def home(request):
    user_text = ""
    ranked_dishes = []

    if request.method == "POST":
        user_text = request.POST.get("userText", "")
        selected_cuisine = request.POST.get("selectedCuisine", "")

        dish_names = [dish.strip().lower() for dish in user_text.split(',') if dish.strip()]

        if dish_names and selected_cuisine:
            stop_words = set(stopwords.words('english'))
            reviews = load_reviews_for_cuisine(selected_cuisine)

            dish_counts = Counter()
            dish_sentiments = {}
            dish_stars = {}

            for review in reviews:
                text = review['text'].lower()
                for dish in dish_names:
                    if dish in text:
                        dish_counts[dish] += 1
                        sentiment = TextBlob(text).sentiment.polarity
                        dish_sentiments.setdefault(dish, []).append(sentiment)
                        dish_stars.setdefault(dish, []).append(float(review.get('stars', 0)))

            dish_scores = {}
            for dish in dish_counts:
                count = dish_counts[dish]
                avg_sentiment = np.mean(dish_sentiments.get(dish, [0]))
                avg_star = np.mean(dish_stars.get(dish, [0]))
                score = 0.5 * count + 0.3 * avg_sentiment + 0.2 * avg_star
                dish_scores[dish] = score

            ranked_dishes = sorted(dish_scores.items(), key=lambda x: -x[1])

    return render(request, "home.html", {
        "user_text": user_text,
        "ranked_dishes": ranked_dishes
    })
