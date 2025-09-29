import requests
import streamlit as st

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="📖 Dictionary App", layout="centered")

# ----------------- CUSTOM CSS -----------------
page_bg = """
<style>
/* Background Gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #E3FDFD, #CBF1F5, #A6E3E9, #71C9CE);
    color: #000000;
}

/* Header */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Text and Headings */
h1, h2, h3, h4, h5, h6, p, span, div {
    color: #1B262C !important;
}

/* Input Box */
.stTextInput > div > div > input {
    border-radius: 12px;
    border: 2px solid #1B6B93;
    background-color: #1B262C;   /* Dark background for input */
    color: #FFFFFF !important;   /* Light text color */
    font-weight: bold;
}

/* Alerts */
.stAlert {
    border-radius: 10px;
    color: #000000 !important;
}

/* Custom Follow Buttons */
.follow-btn {
    background-color: #0F4C75;
    color: #FFFFFF !important;
    border-radius: 8px;
    padding: 0.5em 1em;
    text-align: center;
    font-weight: bold;
    width: 100%;
    display: inline-block;
    text-decoration: none;
}
.follow-btn:hover {
    background-color: #3282B8;
    color: #FFFFFF !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----------------- TITLE -----------------
st.markdown("<h1 style='text-align:center; color:#0F4C75;'>📖 Stylish Dictionary App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px; color:#1B262C;'>Type any English word and get its meaning, pronunciation, and example sentences.</p>", unsafe_allow_html=True)

# ----------------- INPUT -----------------
word = st.text_input("🔍 Enter a word:", "").strip()

if word:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]

        # ----------------- WORD & PRONUNCIATION -----------------
        word_text = data["word"].capitalize()
        pronunciation = "N/A"
        audio_link = None
        phonetics = data.get("phonetics", [])
        for p in phonetics:
            if "text" in p and pronunciation == "N/A":
                pronunciation = p["text"]
            if "audio" in p and p["audio"]:
                audio_link = p["audio"]
                break

        st.markdown(f"<h2 style='color:#0F4C75;'>📌 {word_text}</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"🔊 Pronunciation: `{pronunciation}`")
        with col2:
            if audio_link:
                st.audio(audio_link, format="audio/mp3")

        # ----------------- MAIN MEANING -----------------
        meanings = data["meanings"]
        main_def = meanings[0]["definitions"][0]["definition"]
        example = meanings[0]["definitions"][0].get("example")

        st.success(f"💡 {main_def}")
        if example:
            st.markdown(f"<p style='color:#222831;'><b>✏️ Example:</b> {example}</p>", unsafe_allow_html=True)
        else:
            st.info("No example available for this word.")

        # ----------------- EXTRA MEANINGS -----------------
        with st.expander("📚 Show more meanings"):
            for meaning in meanings:
                part_of_speech = meaning["partOfSpeech"].capitalize()
                st.markdown(f"<h4 style='color:#0F4C75;'>➡️ {part_of_speech}</h4>", unsafe_allow_html=True)
                for idx, definition in enumerate(meaning["definitions"][:3], start=1):
                    st.write(f"{idx}. {definition['definition']}")
                    if "example" in definition:
                        st.markdown(f"<p style='color:#393E46;'>✏️ {definition['example']}</p>", unsafe_allow_html=True)
    else:
        st.error("❌ Word not found. Try another one.")

# ----------------- FOOTER -----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px; color:#1B262C;'>Made by Vedant Vashishtha 😊</p>", unsafe_allow_html=True)

# ----------------- FOLLOW LINKS -----------------
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        "<a href='https://www.linkedin.com/in/vedant-vashishtha-4933b3301/' target='_blank' class='follow-btn'>🔗 LinkedIn</a>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<a href='https://github.com/VedantVas' target='_blank' class='follow-btn'>💻 GitHub</a>",
        unsafe_allow_html=True
    )
