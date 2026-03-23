import streamlit as st
from google import genai
from PIL import Image
import urllib.parse
import requests
from io import BytesIO

# Page Setup
st.set_page_config(page_title="AungMyinMhu AI Architect Pro", layout="centered")

# --- API KEY CONFIG ---
# လူကြီးမင်း၏ API Key ကို ဒီနေရာမှာ သေချာထည့်ပါ
MY_API_KEY = "AIzaSyCiECGk368a5xVYmI5ZNwTj7exGCVr5yYw"
client = genai.Client(api_key=MY_API_KEY)

st.markdown("<h1 style='text-align: center; color: #d4af37;'>🏠 AungMyinMhu AI Architect</h1>", unsafe_allow_html=True)
st.write("---")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    plot_size = st.text_input("📏 မြေကွက်အကျယ် (ပေ)", "40ft x 60ft")
    floors = st.selectbox("🏢 အလွှာအရေအတွက်", ["၁ ထပ်", "၂ ထပ်", "၃ ထပ်", "ထပ်ခိုးပါ"])
with col2:
    # --- အိပ်ခန်းအရေအတွက် ထည့်သွင်းခြင်း ---
    rooms = st.text_input("🛌 အိပ်ခန်းအရေအတွက်", "3 Bedrooms, 2 Bathrooms")
    style = st.selectbox("🎨 ဗိသုကာစတိုင်", ["Modern Minimalism", "Luxury Modern", "Classic European", "Tropical Burmese"])

# --- စိတ်ကြိုက် Prompt ရေးနိုင်သည့်နေရာ ---
custom_notes = st.text_area("✍️ အခြားအသေးစိတ် လိုချင်တာများ (Custom Prompt)", 
                            placeholder="ဥပမာ - ရေကူးကန်ပါရမယ်၊ အိမ်ရှေ့မှာ ခြံဝင်းအကျယ်ကြီးထားပေးပါ၊ အမိုးက အပြာရောင်ဖြစ်ရမယ်...")

uploaded_file = st.file_uploader("📸 Reference အိမ်ပုံထည့်ရန် (Optional)", type=["jpg", "png", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Reference ပုံ", width=300)

if st.button("✨ ဒီဇိုင်းသစ် ထုတ်လုပ်ရန်"):
    if "YOUR" in MY_API_KEY:
        st.error("API Key ထည့်ဖို့ မမေ့ပါနဲ့ဦးဗျ။")
    else:
        with st.spinner("AI စနစ်အသစ်ဖြင့် ပုံဖော်ပေးနေပါသည်..."):
            try:
                # Prompt တည်ဆောက်ခြင်း
                prompt_text = (f"Professional Architect for AungMyinMhu Construction. "
                               f"Generate 1 high-quality exterior image prompt for a {style} style {floors} home "
                               f"on a {plot_size} plot with {rooms}. ")
                
                if custom_notes:
                    prompt_text += f"Additional Requirements: {custom_notes}. "
                
                contents_list = [prompt_text]
                if uploaded_file:
                    contents_list.append(img)
                
                # Gemini 2.0 Flash ကို သုံးထားပါသည်
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=contents_list
                )
                
                generated_prompt = response.text
                
                # Image Generation (Pollinations AI)
                encoded_prompt = urllib.parse.quote(generated_prompt[:250])
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=42"
                
                st.success("အောင်မြင်စွာ ထုတ်လုပ်ပြီးပါပြီ!")
                st.image(image_url, caption="AungMyinMhu New Design", use_column_width=True)
                
                # --- Download Button ထည့်သွင်းခြင်း ---
                img_response = requests.get(image_url)
                btn = st.download_button(
                    label="📥 ဒီဇိုင်းပုံကို သိမ်းဆည်းရန်",
                    data=img_response.content,
                    file_name="AungMyinMhu_Design.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"Error: {e}")

st.write("---")
st.caption("© 2026 AungMyinMhu Construction | Powered by Gemini 2.0 Flash")

