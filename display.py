import streamlit as st

def show_recommendations(recommendations):
    for _, row in recommendations.iterrows():
        title = row.get('title', 'Unknown Title')
        release_date = row.get('release_date', 'N/A')
        runtime = row.get('runtime', 'N/A')
        original_language = row.get('original_language', 'N/A')
        overview = row.get('overview', 'No overview available.')
        imdb_rating = row.get('imdb_rating', 'N/A')
        poster = row.get('poster_path', '')

        #Title
        st.markdown(f"**🎬 {title}**")

        # Details
        st.caption(f"🗓️ Release Date: {release_date} | ⏱️ Runtime: {runtime} min | 🌐 Language: {original_language} | ⭐ IMDb: {imdb_rating}")
        
        # Overview
        st.write(f"**Overview:** {overview}")

        # Poster    
        if poster:
            st.image(f"https://image.tmdb.org/t/p/w300{poster}", use_container_width=False)

        
        st.markdown("---") 