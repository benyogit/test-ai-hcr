import streamlit as st
import numpy as np
from PIL import Image
import requests
import google.generativeai as genai

# הגדרות דף בסיסיות
st.set_page_config(page_title="עוזר הוראה חכם - Gemini", layout="wide")

# הגדרת API
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ מפתח API לא נמצא בהגדרות המערכת.")
    st.stop()

genai.configure(api_key=api_key)

# סינון מודלים שמתחילים ב-models/ ותומכים בראייה
try:
    models = genai.list_models()
    model_names = [m.name for m in models if "generateContent" in m.supported_generation_methods and m.name.startswith("models/")]
except Exception:
    # Fallback למקרה של תקלה ברשימה
    model_names = ["models/gemini-1.5-flash", "models/gemini-1.5-pro"]

# --- ממשק משתמש בעברית ---
st.title("🍎 עוזר הוראה חכם: בדיקת מבחנים ב-Gemini")
st.markdown("""
מערכת זו עוזרת למורים לפענח כתב יד של תלמידים ולבדוק אותם מול מחוון (Rubric) מוגדר מראש.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("⚙️ הגדרות בדיקה")
    selected_model = st.selectbox("בחר מודל Gemini:", model_names, index=0)
    
    # דוגמה למחוון בהיסטוריה של עם ישראל
    default_rubric = """מחוון לבדיקת שאלה על העלייה הראשונה והשנייה:
1. זיהוי שנים (5 נק'): ציון שנות העלייה הראשונה (1881-1903).
2. מניעי עלייה (10 נק'): אזכור 'סופות בנגב' או רדיפות באירופה.
3. מאפייני עולים (10 נק'): ציון כי רובם היו משפחות דתיות/מסורתיות.
4. קשיים (5 נק'): אזכור מלריה, חוסר ניסיון חקלאי או עימותים עם השלטון העות'מאני.
ציון מקסימלי: 30 נקודות."""

    user_rubric = st.text_area("הכנס את המחוון (הנחיות הבדיקה):", value=default_rubric, height=250)

with col2:
    st.subheader("📸 העלאת תשובת תלמיד")
    uploaded_file = st.file_uploader("העלה צילום של כתב היד:", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="תמונת התשובה", use_container_width=True)
    else:
        st.info("אנא העלה תמונה כדי להתחיל בבדיקה.")

# כפתור הפעלה
if st.button("בצע בדיקה ומתן ציון"):
    if not uploaded_file:
        st.warning("⚠️ לא הועלתה תמונה של תשובת תלמיד.")
    elif not user_rubric.strip():
        st.warning("⚠️ נא להזין מחוון בדיקה.")
    else:
        try:
            with st.spinner("Gemini מנתח את כתב היד ומחשב ציון..."):
                model = genai.GenerativeModel(selected_model)
                
                # בניית הפרומפט המקצועי
                prompt = f"""
                אתה עוזר הוראה מומחה במערכת החינוך הישראלית.
                משימתך:
                1. פענח ותמלל את כתב היד בעברית מהתמונה המצורפת.
                2. בדוק את התשובה מול המחוון הבא:
                {user_rubric}
                
                פורמט תשובה נדרש:
                - תמלול התשובה (מה כתב התלמיד).
                - ניתוח לפי סעיפי המחוון.
                - ציון סופי.
                - הערות לשיפור עבור התלמיד.
                
                השב בעברית ברורה ורהוטה.
                """
                
                response = model.generate_content([prompt, image])
                
                st.divider()
                st.subheader("📝 דו''ח בדיקה:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"שגיאה בתהליך: {e}")