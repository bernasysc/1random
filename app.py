import streamlit as st
from logic.recommender import load_data, get_movies_by_genre, get_main_genre_display, get_subgenre_display
from ui.display import show_recommendations


# Load data
df = load_data("data/TMDB_all_movies.csv")


# Title 
st.title("Movie Recommender 🎬🍿")


 
# ------------------------ FILTER/SELECTION UI  ------------------------
# Genre selection with emojis
selected_main_genre_display = st.selectbox("Choose a genre:", get_main_genre_display())
selected_main_genre = selected_main_genre_display.split(" ", 1)[1]

selected_subgenre_display = st.selectbox("Optional: subgenre", ["All"] + get_subgenre_display())
selected_subgenre = selected_subgenre_display.split(" ", 1)[1] if selected_subgenre_display != "All" else None


#Country selection
country_options = {
    "🗽 USA": "en",
    "🎡 UK": "en",           # same language code as USA 
    "🥐 France": "fr",
    "🍜 South Korea": "ko",
    "🕌 India": "hi",
    "🐉 China": "zh"
}

# Country selectbox with 'All' and 'Other'
selected_country_display = st.selectbox(
    "Choose a country:",
    ["All"] + list(country_options.keys()) + ["🌍 Other"]
)

# Convert display choice to language code or 'Other' or None
if selected_country_display in country_options:
    selected_country = country_options[selected_country_display]   # e.g. "en", "fr"
elif selected_country_display == "Other":
    selected_country = "Other"
else:
    selected_country = None


#Runtime selection
runtime_ranges = {
    "Any length": (0, None),
    "< 60 min": (0, 60),
    "< 90 min": (60, 90),
    "< 120 min": (90, 120),
    "< 150 min": (120, 150),
    "< 180 min": (150, 180)
}

selected_runtime_display = st.selectbox(
    "Choose movie length:",
    list(runtime_ranges.keys())
)

selected_runtime_min, selected_runtime_max = runtime_ranges[selected_runtime_display]


# IMDb rating selection
rating_options = {
    "Any rating": (0, 10),
    "⭐ 9+ (Masterpieces)": (9, 10),
    "⭐ 8–9 (Excellent)": (8, 9),
    "⭐ 7–8 (Good)": (7, 8),
    "⭐ 6–7 (Average)": (6, 7),
    "⭐ Below 6 (Low-rated)": (0, 6)
}

selected_rating_display = st.selectbox(
    "Choose IMDb rating range:",
    list(rating_options.keys())
)

selected_rating_min, selected_rating_max = rating_options[selected_rating_display]



# ------------------------FILTER/SELECTION LOGIC ------------------------
if st.button("Recommend movies"):

    # Main genre filter
    recommendations = df[df['genres'].str.contains(selected_main_genre, case=False, na=False)]

    # Optional subgenre filter
    if selected_subgenre:
        recommendations = recommendations[recommendations['overview'].str.contains(selected_subgenre, case=False, na=False)]
    
    # Country filter
    if selected_country != "All":
        recommendations = recommendations[recommendations['original_language'] == selected_country]

    # Runtime filter
    if selected_runtime_display != "Any length":
        if selected_runtime_max is not None:
            recommendations = recommendations[
                (recommendations['runtime'] >= selected_runtime_min) &
                (recommendations['runtime'] < selected_runtime_max)
            ]

    # IMDb rating filter
    if selected_rating_display != "Any rating":
        recommendations = recommendations[
            (recommendations['imdb_rating'] >= selected_rating_min) &
            (recommendations['imdb_rating'] < selected_rating_max)
        ]


# ----------------------- DISPLAYING MOVIES -----------------------

    if recommendations.empty:
        st.warning("No movies found.")

    else:
        st.markdown(f"### Recommended Movies")
        for _, row in recommendations.sample(min(10, len(recommendations))).iterrows():
            st.markdown(f"**{row['title']}** — {row['release_date']} | ⏱️ {row['runtime']} min | 🌐 {row['original_language']} | ⭐ {row['imdb_rating']}")

            st.write(f"**Overview:** {row['overview']}")    

            #Poster 
            if row['poster_path']:
                st.image(f"https://image.tmdb.org/t/p/w300{row['poster_path']}", use_container_width=False)
        
        
            st.markdown("---")
