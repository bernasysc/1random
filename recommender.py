import pandas as pd
import ast


# Emojis for main genres 
MAIN_GENRE_EMOJIS = {
    "Science Fiction": "🚀",
    "Fantasy": "🧙‍♂️", 
    "Horror": "💀", 
    "Action": "💥", 
    "Animation": "🎨", 
    "Comedy": "🎭", 
    "Drama": "👨‍👩‍👧‍👦", 
    "Romance": "💕",
    "Documentary": "🎥"
}

# Emojis for subgenres
SUBGENRE_EMOJIS = {
    "Thriller": "😱",
    "Teenage": "🤟",
    "Mystery": "🔍",
    "Psychological": "🧠",
    "War": "⚔️",
    "Slasher": "🔪",
    "Sports": "🏀",
    "Crime": "🕵️‍♂️",
    "Family": "👨‍👩‍👧‍👦",
    "Music": "🎵",
    "Western": "🐎" 
}


#Assigning subgenres 
def assign_subgenre(row):
    text = (row['genres'] + " " + row['overview']).lower()
    assigned = []

    if "animation" in text or "animated" in text or "cartoon" in text or "anime" in text:
        assigned.append("Animated")
    if "psychological" in text or "mind" in text or "mental" in text:
        assigned.append("Psychological")
    if "teen" in text or "high school" in text or "young adult" in text or "adolescent" in text:
        assigned.append("Teenage")
    if "mystery" in text or "detective" in text or "whodunit" in text or "suspense" in text:
        assigned.append("Mystery")
    if "war" in text or "battle" in text or "army" in text or "soldier" in text or "combat" in text:
        assigned.append("War")
    if "slasher" in text or "killer" in text or "murder" in text or "stalker" in text:
        assigned.append("Slasher")
    if "sports" in text or "football" in text or "basketball" in text or "soccer" in text or "athlete" in text:
        assigned.append("Sports")
    if "crime" in text or "gangster" in text or "detective" in text or "heist" in text or "robbery" in text:
        assigned.append("Crime")
    if "family" in text or "children" in text or "kid" in text or "parent" in text or "siblings" in text:
        assigned.append("Family")
    if "music" in text or "musical" in text or "band" in text or "song" in text or "concert" in text:
        assigned.append("Music")
    if "western" in text or "cowboy" in text or "outlaw" in text or "sheriff" in text or "ranch" in text:
        assigned.append("Western")
    if "thriller" in text or "suspense" in text or "chase" in text or "danger" in text or "mystery" in text:
        assigned.append("Thriller")

    

    return " ".join(assigned) if assigned else ""


# Load data
def load_data(csv_path):

    use_cols = [
        'title', 'release_date', 'runtime', 'original_language',
        'overview', 'genres', 'imdb_rating', 'poster_path'
    ]

    chunksize = 100_000  # number of rows per chunk
    chunks = pd.read_csv(csv_path, usecols=use_cols, chunksize=chunksize)

    processed_chunks = []  

    for chunk in chunks:
        # Clean column names
        chunk.columns = chunk.columns.str.strip().str.lower()

        # Fill missing values
        chunk['title'] = chunk['title'].fillna('')
        chunk['overview'] = chunk['overview'].fillna('')
        chunk['genres'] = chunk['genres'].fillna('').astype(str).str.replace(',', ' ')

        # Create combined features column for recommendations
        chunk['features'] = chunk['genres'] + ' ' + chunk['overview']

        # If you use subgenres later
        if 'subgenres' not in chunk.columns:
            chunk['subgenres'] = ''

        processed_chunks.append(chunk)

    # Combine all chunks into one DataFrame
    df = pd.concat(processed_chunks, ignore_index=True)

    return df



#Get movies by genre 
def get_movies_by_genre(df, genre, limit=10):
    """Return up to 'limit' movies that match the selected genre."""
    genre = genre.lower()
    results = df[df['genres'].str.lower().str.contains(genre, na=False)]
    return results.sample(min(limit, len(results))) if not results.empty else pd.DataFrame()


# Display for maingenres and subgenres
def get_main_genre_display():
    """Return formatted list for main genres like ['🚀 Science Fiction', '😂 Comedy']"""
    return [f"{emoji} {genre}" for genre, emoji in MAIN_GENRE_EMOJIS.items()]

def get_subgenre_display():
    """Return formatted list for subgenres like ['🧠 Psychological', '🔍 Mystery']"""
    return [f"{emoji} {genre}" for genre, emoji in SUBGENRE_EMOJIS.items()]
