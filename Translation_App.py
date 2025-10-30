import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pyperclip
import os

# ------------------------------
# Supported languages (Deep Translator)
# ------------------------------
LANGUAGES = GoogleTranslator(source='auto', target='english').get_supported_languages(as_dict=True)

LANGUAGE_NAMES = list(LANGUAGES.keys())

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Universal Language Translator", page_icon="🌍")
st.title("🌍 Universal Translator — Translate Between Any Languages")

st.markdown("Translate text between **any two languages** instantly using Google Translate API.")

# Input text
text = st.text_area("📝 Enter text to translate:")

# Language selection
source_lang = st.selectbox("🌐 Source language:", ["auto"] + LANGUAGE_NAMES)
target_lang = st.selectbox("🎯 Target language:", LANGUAGE_NAMES, index=LANGUAGE_NAMES.index("english") if "english" in LANGUAGE_NAMES else 0)

# Translate button
if st.button("Translate"):
    if text.strip():
        try:
            # Perform translation
            translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)

            # Display result
            st.success("✅ Translated Text:")
            st.write(translated_text)

            # Buttons: copy and speech
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy Translated Text"):
                    pyperclip.copy(translated_text)
                    st.info("Copied to clipboard!")
            with col2:
                if st.button("🔊 Speak Translation"):
                    try:
                        # Try to play speech
                        tts = gTTS(translated_text, lang=LANGUAGES[target_lang])
                        tts.save("translated.mp3")
                        audio_file = open("translated.mp3", "rb")
                        st.audio(audio_file.read(), format="audio/mp3")
                        audio_file.close()
                        os.remove("translated.mp3")
                    except Exception as e:
                        st.warning("⚠️ Text-to-speech may not support this language.")
        except Exception as e:
            st.error(f"⚠️ Translation failed: {e}")
    else:
        st.warning("Please enter some text to translate.")
