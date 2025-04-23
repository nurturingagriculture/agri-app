import streamlit as st
from PIL import Image
import io
from modules import ai_bot, schemes
from modules.crop_disease_detector import predict_crop_disease
import pandas as pd
from style import load_style, footer
from modules.news_fetcher import scrapper 

load_style()

# Load the CSV file
def load_news_data(file_path):
    return pd.read_csv(file_path)

# Display news in card format
def display_news(news_df):
    for _, row in news_df.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9;">
                    <h4 style="color:#2E7D32;">{row['Title']}</h4>
                    <p>{row['Desc']}</p>
                    <a href="{row['Link']}" target="_blank" style="color:#1E88E5; text-decoration:none;">Read more</a>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["AI Chatbot", "Crop Disease Detection", "Government Schemes", "Agricultural News"])

# --- 1. AI Chatbot Section ---
if section == "AI Chatbot":
    st.markdown("<h1 class='main-title'>Agricultural Assistant Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("Ask questions about crops, soil, and diseases. You can also optionally upload an image for crop disease queries.")
    ai_bot.chatbot_ui()

# --- 2. Crop Disease Detection Section ---
elif section == "Crop Disease Detection":
    st.markdown("<h1 class='main-title'>🌿 Crop Disease Detection</h1>", unsafe_allow_html=True)
    st.markdown("Upload an image of your crop to detect diseases and get treatment recommendations.")
    uploaded_image = st.file_uploader("📤 Upload Crop Image", type=["jpg", "jpeg", "png"], key="crop_upload")
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Crop Image", width=300)
        if st.button("🔍 Detect Disease"):
            with st.spinner("Analyzing the image... Please wait."):
                try:
                    results = predict_crop_disease(image)
                    st.subheader("🩺 Prediction Results")
                    st.write(f"**Disease:** {results['disease']}")
                    st.write(f"**Confidence:** {results['confidence'] * 100:.1f}%")
                    if "remedy" in results:
                        st.markdown("### 💊 Treatment Recommendation")
                        st.write(results["remedy"])
                        st.write("**Marathi Translation:**")
                        st.write(results["remedy_translation"])
                    else:
                        st.write("The plant appears to be healthy. No treatment necessary.")
                    if results.get("alternatives"):
                        st.markdown("**Alternative Possibilities:**")
                        for alt in results["alternatives"]:
                            st.write(f"- {alt['disease']} (Confidence: {alt['confidence'] * 100:.1f}%)")
                except Exception as e:
                    st.error(f"🚨 An error occurred while processing the image: {e}")

# --- 3. Government Schemes Section ---
elif section == "Government Schemes":
    st.markdown("<h1 class='main-title'>Government Schemes Assistant Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("Ask questions to get most out of the Government Schemes")
    schemes.chatbot_ui()


# --- 4. Agricultural News Section ---
elif section == "Agricultural News":
    news_data = load_news_data("assets/agriculture_news.csv")
    st.subheader("Latest Agricultural News")
    display_news(news_data)

    if st.button("Fetch Latest"):
        scrapper()
        st.success("Latest news fetched successfully!")



