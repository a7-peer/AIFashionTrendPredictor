import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from config import REPLICATE_API_TOKEN, OLLAMA_MODEL
from ollama_predictor import TrendPredictor
from replicate_generator import FashionImageGenerator
from trend_data import get_trend_data
import os

# Initialize components
predictor = TrendPredictor()
generator = FashionImageGenerator()

st.set_page_config(page_title="🇵🇰 Fashion Trend Predictor", layout="wide")

# Sidebar configuration
with st.sidebar:
    st.title("Configuration")
    st.markdown(f"""
    - **Ollama Model**: `{OLLAMA_MODEL}`
    - **Image Engine**: Replicate SDXL
    """)
    if st.button("🔄 Clear Cache"):
        st.cache_data.clear()

# Main title
st.title("👗 Pakistani Fashion Trend Predictor")

# Load Google Trends data
@st.cache_data
def load_trend_data():
    return get_trend_data()

try:
    trend_data = load_trend_data()
    st.line_chart(trend_data)
except Exception as e:
    st.error(f"❌ Failed to load trend data: {str(e)}")
    st.stop()

# Prediction and image generation
if st.button("🔮 Predict Trends", type="primary"):
    with st.spinner("Analyzing trends with Ollama..."):
        try:
            prediction = predictor.predict(trend_data.to_string())
            st.subheader("📈 Predicted Fashion Trends")
            st.markdown(prediction)

            # Get top 3 trends from the prediction
            trends = [line.split(':', 1)[0].strip() for line in prediction.split('\n')
                      if line.strip() and line[0].isdigit()][:3]

            st.subheader("🧵 AI-Generated Fashion Concepts")
            cols = st.columns(len(trends))

            for idx, trend in enumerate(trends):
                with cols[idx]:
                    with st.spinner(f"Creating image for: {trend}"):
                        try:
                            # Try generating image with Replicate
                            img_url = generator.generate(trend)
                            response = requests.get(img_url)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, caption=trend, use_column_width=True)

                            st.download_button(
                                "⬇️ Download",
                                response.content,
                                file_name=f"pakistani_{trend.replace(' ', '_')}.png",
                                mime="image/png"
                            )

                        except Exception as e:
                            st.error(f"❌ Image generation failed for '{trend}': {str(e)}")

                            # Optional: Use a placeholder image
                            placeholder_url = f"https://via.placeholder.com/300x200.png?text={trend.replace(' ', '+')}"
                            st.image(placeholder_url, caption=f"{trend} (Placeholder)", use_column_width=True)

                            # Google Images search fallback
                            st.markdown(
                                f"🔍 **Explore more styles on Google Images:** "
                                f"[Click here](https://www.google.com/search?tbm=isch&q=Pakistani+{trend.replace(' ', '+')}+fashion)"
                            )

        except Exception as e:
            st.error(f"❌ Trend prediction failed: {str(e)}")
