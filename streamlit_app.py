import streamlit as st
import google.generativeai as genai

# App title
st.title("👾 AI-powered Anime Recommendation Chatbot")

# Capture Gemini API Key
gemini_api_key = "AIzaSyCI2Z6UzDbE2Sv1zBjnpRRfZkXmFWRStqk"

# Initialize the Gemini Model
if gemini_api_key:
    try:
        # Configure the API with the provided key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")  # Use Gemini model for generating responses
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"Error setting up the Gemini model: {e}")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Dictionary of anime recommendations (can be used alongside AI responses)
anime_recommendations = {
    "action": ["Attack on Titan", "Naruto", "Demon Slayer"],
    "fantasy": ["Sword Art Online", "Fullmetal Alchemist", "Re:Zero"],
    "romance": ["Your Lie in April", "Toradora", "Clannad"],
    "adventure": ["One Piece", "Hunter x Hunter", "Made in Abyss"],
    "comedy": ["Gintama", "KonoSuba", "The Disastrous Life of Saiki K."]
}

# Function to get recommendations based on genre
def get_anime_recommendations(genre):
    return anime_recommendations.get(genre.lower(), ["Sorry, I don't have recommendations for that genre."])

# Input for user message
user_input = st.text_input("Ask for anime recommendations or type your message:")

# Process user input
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    # Check if API Key is provided and model is set up
    if gemini_api_key and model:
        try:
            # Generate AI-based response
            response = model.generate_content(user_input)
            bot_response = response.text
            st.session_state.chat_history.append(("assistant", bot_response))
            st.write(f"**AI Bot:** {bot_response}")
        except Exception as e:
            st.error(f"Error generating AI response: {e}")
    else:
        # Use predefined anime recommendations if no AI response
        if "recommend" in user_input.lower():
            genre = user_input.split()[-1].lower()  # Assumes the last word is the genre
            bot_response = get_anime_recommendations(genre)
        else:
            bot_response = ["I'm not sure how to respond to that. Try asking for an anime recommendation!"]

        # Append bot response to chat history
        st.session_state.chat_history.append(("assistant", ", ".join(bot_response)))
        st.write(f"**Bot:** {', '.join(bot_response)}")

# You can comment this section out if you don't want to display chat history
# Display chat history
# st.write("**Chat History:**")
# for sender, message in st.session_state.chat_history:
#     if sender == "user":
#         st.write(f"**You:** {message}")
#     else:
#         st.write(f"**Bot:** {message}")

