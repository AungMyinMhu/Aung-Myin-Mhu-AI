import streamlit as st
import google.generativeai as genai
import urllib.parse

# Page Configuration
st.set_page_config(page_title="AungMyinMhu AI Architect Pro", layout="centered")

# --- API KEY CONFIG ---
# လူကြီးမင်း၏ API Key ကို ဒီမှာ ထည့်သွင်းပါ
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)

# --- APP UI ---
st.markdown("<h1 style='text-align: center; color: #d4af37;'>🏠 AungMyinMhu AI Architect Pro</h1>", unsafe_content_factory=True)
st.write("---")

# Input Section
col1, col2 = st.columns(2)
with col1:
    plot_size = st.text_input("📏 မြေကွက်အကျယ် (ပေ)", "40ft x 60ft")
    floors = st.selectbox("🏢 အလွှာအရေအတွက်", ["၁ ထပ်", "၂ ထပ်", "၃ ထပ်", "ထပ်ခိုးပါ"])
with col2:
    rooms = st.text_input("🛌 အခန်းအရေအတွက်", "3 Bedrooms, 2 Bathrooms")
    style = st.selectbox("🎨 ဗိသုကာစတိုင်", ["Modern Minimalism", "Luxury Modern", "Classic European", "Tropical Burmese"])

# Generate Button
if st.button("✨ အိမ်ဒီဇိုင်းနှင့် Floor Plan အလိုအလျောက် ထုတ်ယူရန်"):
    with st.spinner("AI မှ ပုံဖော်ပေးနေပါသည်... ခဏစောင့်ပါ..."):
        try:
            # 1. Gemini Pro ဖြင့် Prompt ထုတ်ယူခြင်း
            model = genai.GenerativeModel('gemini-1.5-pro')
            system_instruction = f"Architect for AungMyinMhu Construction. Generate 1 short, detailed image prompt for a {style} style {floors} home on {plot_size} plot with {rooms}. Focus on visual beauty."
            
            response = model.generate_content(system_instruction)
            generated_prompt = response.text
            
            # 2. ပုံထုတ်ရန် URL ပြင်ဆင်ခြင်း (Using Pollinations.ai - Free Image API)
            encoded_prompt = urllib.parse.quote(generated_prompt)
            # 3D Exterior Image
            image_url_3d = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true"
            # 2D Floor Plan Image (Prompt ကို အနည်းငယ် ပြင်ဆင်ခြင်း)
            floor_plan_prompt = urllib.parse.quote(f"Professional 2D floor plan blueprint for {plot_size} {floors} home, {rooms}, black and white technical drawing, architecture style.")
            image_url_2d = f"https://image.pollinations.ai/prompt/{floor_plan_prompt}?width=1024&height=1024&nologo=true"

            # 3. ရလဒ်များကို ပြသခြင်း
            st.success("အောင်မြင်စွာ ထုတ်လုပ်ပြီးပါပြီ!")
            
            st.subheader("🎨 3D Exterior View")
            st.image(image_url_3d, caption=f"AungMyinMhu {style} Design", use_column_width=True)
            
            st.subheader("📋 2D Floor Plan (Blueprint)")
            st.image(image_url_2d, caption="Architectural Layout", use_column_width=True)
            
            st.info(f"**AI Prompt:** {generated_prompt}")

        except Exception as e:
            st.error(f"Error တက်သွားပါသည်: {e}")

st.write("---")
st.caption("© 2026 AungMyinMhu Construction | Powered by Gemini Pro")
