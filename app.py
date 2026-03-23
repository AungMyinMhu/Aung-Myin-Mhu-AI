import streamlit as st
import google.generativeai as genai
import urllib.parse
from PIL import Image

# Page Config
st.set_page_config(page_title="AungMyinMhu AI Architect", layout="centered")

# --- API KEY (ဒီနေရာမှာ လူကြီးမင်းရဲ့ API Key သေချာထည့်ပါ) ---
API_KEY = "AIzaSyCiECGk368a5xVYmI5ZNwTj7exGCVr5yYw" 
genai.configure(api_key=API_KEY)

st.markdown("<h1 style='text-align: center; color: #d4af37;'>🏠 AungMyinMhu AI Architect</h1>", unsafe_allow_html=True)
st.write("---")

# Inputs
plot_size = st.text_input("📏 မြေကွက်အကျယ်", "40ft x 60ft")
floors = st.selectbox("🏢 အလွှာ", ["၁ ထပ်", "၂ ထပ်", "၃ ထပ်"])
style = st.selectbox("🎨 စတိုင်", ["Modern Minimalism", "Luxury Modern", "Tropical Burmese"])

uploaded_file = st.file_uploader("📸 Reference ပုံထည့်ရန်", type=["jpg", "png", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="လူကြီးမင်း ထည့်လိုက်သော Reference ပုံ", width=300)

if st.button("✨ ဒီဇိုင်းသစ် ထုတ်လုပ်ရန်"):
    if not API_KEY or "YOUR" in API_KEY:
        st.error("API Key ကို GitHub မှာ သေချာပြန်ထည့်ပေးပါဦးဗျ။")
    else:
        with st.spinner("AI မှ ပုံဖော်ပေးနေပါသည်..."):
            try:
                # 2026 ခုနှစ်အတွက် နောက်ဆုံးထွက် Model နာမည်များကို အစဉ်လိုက် စမ်းသပ်ခြင်း
                # တစ်ခုခု Error တက်ရင် နောက်တစ်ခုကို အလိုအလျောက် ပြောင်းသုံးပါလိမ့်မယ်
                models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                
                response = None
                prompt = f"Architect for AungMyinMhu Construction. {style} {floors} home on {plot_size} plot. High quality exterior design."
                
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name)
                        if uploaded_file:
                            response = model.generate_content([prompt, img])
                        else:
                            response = model.generate_content(prompt)
                        if response: break
                    except:
                        continue
                
                if response:
                    # Image Generation (Pollinations AI)
                    clean_text = response.text.replace("\n", " ").strip()[:200]
                    encoded_prompt = urllib.parse.quote(clean_text)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                    
                    st.success("အောင်မြင်စွာ ထုတ်လုပ်ပြီးပါပြီ!")
                    st.image(image_url, use_column_width=True)
                else:
                    st.error("Model ချိတ်ဆက်မှု အဆင်မပြေပါ။ ခဏနေမှ ပြန်စမ်းကြည့်ပါဗျ။")
            
            except Exception as e:
                st.error(f"Error: {e}")

st.write("---")
st.caption("© 2026 AungMyinMhu Construction")
