import streamlit as st
import google.generativeai as genai
import urllib.parse
from PIL import Image

# Page Configuration
st.set_page_config(page_title="AungMyinMhu AI Architect Pro", layout="centered")

# --- API KEY CONFIG ---
# လူကြီးမင်း၏ API Key ကို ဒီနေရာမှာ သေချာပြန်ထည့်ပေးပါဗျ
GEMINI_API_KEY = "AIzaSyCiECGk368a5xVYmI5ZNwTj7exGCVr5yYw" 
genai.configure(api_key=GEMINI_API_KEY)

# Title with HTML
st.markdown("<h1 style='text-align: center; color: #d4af37;'>🏠 AungMyinMhu AI Architect</h1>", unsafe_allow_html=True)
st.write("---")

# Input Section
col1, col2 = st.columns(2)
with col1:
    plot_size = st.text_input("📏 မြေကွက်အကျယ် (ပေ)", "40ft x 60ft")
    floors = st.selectbox("🏢 အလွှာအရေအတွက်", ["၁ ထပ်", "၂ ထပ်", "၃ ထပ်", "ထပ်ခိုးပါ"])
with col2:
    rooms = st.text_input("🛌 အခန်းအရေအတွက်", "3 Bedrooms, 2 Bathrooms")
    style = st.selectbox("🎨 ဗိသုကာစတိုင်", ["Modern Minimalism", "Luxury Modern", "Classic European", "Tropical Burmese"])

# --- IMAGE REFERENCE UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📸 Reference အိမ်ပုံရှိလျှင် ထည့်ပေးပါ (Optional)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="လူကြီးမင်း ထည့်လိုက်သော Reference ပုံ", width=300)

# Generate Button
if st.button("✨ ဒီဇိုင်းအသစ် ဖန်တီးရန်"):
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        st.error("ကျေးဇူးပြု၍ API Key ကို GitHub က app.py ထဲမှာ သေချာထည့်ပေးပါဗျ။")
    else:
        with st.spinner("AI မှ ပုံကို လေ့လာပြီး ဒီဇိုင်းဆွဲပေးနေပါသည်..."):
            try:
                # 404 မဖြစ်စေရန် gemini-1.5-flash သို့ ပြောင်းလဲထားပါသည်
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Professional Architect for AungMyinMhu Construction. Generate 1 short, detailed image prompt for a {style} style {floors} home on {plot_size} plot with {rooms}."
                
                if uploaded_file is not None:
                    prompt += " Look at the attached image carefully. Maintain the architectural style and colors."
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(prompt)
                
                generated_prompt = response.text
                
                # Image Generation (Pollinations AI)
                encoded_prompt = urllib.parse.quote(generated_prompt)
                image_url_3d = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                st.success("ဒီဇိုင်းအသစ် ထွက်လာပါပြီ!")
                st.image(image_url_3d, caption="AungMyinMhu New Design Result", use_column_width=True)

            except Exception as e:
                st.error(f"Error တက်သွားပါသည်: {e}")

st.write("---")
