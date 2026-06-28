import streamlit as st
from datetime import date

# --- Configuration ---
st.set_page_config(page_title="Daily Sports Trivia", layout="centered")

# --- Optimized CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1329; color: white; }
    .game-title { color: #facc15; font-family: 'Arial Black', sans-serif; font-style: italic; font-weight: 900; text-align: center; font-size: 42px; margin-bottom: 0px; }
    .game-subtitle { color: #94a3b8; font-family: sans-serif; text-align: center; font-size: 14px; margin-top: 5px; margin-bottom: 30px; }

    .grid-card {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        font-weight: bold;
        font-size: 16px;
        text-transform: uppercase;
        text-align: center;
        padding: 10px;
    }

    .card-correct { background-color: #10b981; color: white; font-size: 18px; }
    .card-incorrect { background-color: #f43f5e; color: white; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# --- Define Today's Data ---
TODAY_STR = str(date.today())
DAILY_TRIVIA = {
    TODAY_STR: [
        {"id": 0, "category": "Career Path", "question": "Who is this? Suns-Rockets-Suns-Heat-Raptors-Nets-Bulls-Bucks.", "answer": "Goran Dragic"},
        {
            "id": 1, 
            "category": "Guess who", 
            "question": "Who is pictured here?", 
            "answer": "Devan Dubynk", 
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Devan_Dubnyk_-_Switzerland_vs._Canada%2C_29th_April_2012-3.jpg"

        },
        {"id": 2, "category": "Who is #1", "question": "What MLB player has the most hits since 2015?", "answer": "Freddie Freeman"},
        {"id": 3, "category": "College Sports", "question": "Who was the last #1 overall NBA pick who won a March Madness title the year they were drafted? ", "answer": "Anthony Davis"},
        {"id": 4, "category": "Triple Crown", "question": "Since 2020, two NFL WRs have won the triple crown. Name them? (Order alphabetical by last name: ______ and ______) ", "answer": "Ja'Marr Chase and Cooper Kupp"},
        {"id": 5, "category": "Big Pitcher Moments", "question": "In 2017, what MLB pitcher hit a two run triple to put the Diamondbacks ahead 3 runs in the NL Wild Card?", "answer": "Archie Bradley"},
        {"id": 6, "category": "K Him", "question": "Who was the last pitcher to throw a 20K game (2016)?", "answer": "Max Scherzer"},
        {"id": 7, "category": "Boston Bruins", "question": "Before JJ Peterka, when was the last time the Bruins traded their own first round pick (Name who it was for. Hint: Traded it and then traded for it back later)?", "answer": "Tyler Bertuzzi"},
        {"id": 8, "category": "Under 1K", "question": "What NFL player had over 100 receptions but managed to be under 1,000 receiving yards this past season?", "answer": "Christian McCaffrey"}
    ]
}

questions = DAILY_TRIVIA.get(TODAY_STR, [])

if not questions:
    st.error("No Sports Trivia loaded for today's date yet!")
else:
    # --- Session State Initialization ---
    if 'grid_state' not in st.session_state:
        st.session_state.grid_state = [None] * 9
    if 'active_idx' not in st.session_state:
        st.session_state.active_idx = None
    if 'revealed_error' not in st.session_state:
        st.session_state.revealed_error = False

    # --- UI Header ---
    st.markdown('<h1 class="game-title">DAILY SPORTS TRIVIA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">Daily Trivia Board — ' + TODAY_STR + '</p>', unsafe_allow_html=True)

    # --- VIEW A: Individual Question Mode ---
    if st.session_state.active_idx is not None:
        idx = st.session_state.active_idx
        q_data = questions[idx]

        st.subheader(f"Category: {q_data['category']}")

        # Displays image natively from public web URL if included
        if "image_url" in q_data:
            st.image(q_data["image_url"], use_container_width=True)

        st.write(f"### {q_data['question']}")

        user_guess = st.text_input("Type your answer:", key="guess_input", placeholder="Spelling counts...")

        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.revealed_error:
                if st.button("Submit Guess", type="primary"):
                    # This converts both sides to lowercase so capitalization won't matter!
                    if user_guess.strip().lower() == q_data['answer'].lower():
                        st.session_state.grid_state[idx] = "correct"
                        st.session_state.active_idx = None
                        st.rerun()
                    else:
                        st.session_state.grid_state[idx] = "incorrect"
                        st.session_state.revealed_error = True
                        st.rerun()
        with col2:
            if st.button("Back to Board"):
                st.session_state.active_idx = None
                st.session_state.revealed_error = False
                st.rerun()

        if st.session_state.revealed_error:
            st.error(f"❌ Incorrect! The correct answer was: **{q_data['answer']}**")

    # --- VIEW B: Base Grid View ---
    else:
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                q = questions[idx]
                state = st.session_state.grid_state[idx]
                with cols[col]:
                    if state == "correct":
                        st.markdown(f'<div class="grid-card card-correct">✓ {q["category"]}</div>', unsafe_allow_html=True)
                    elif state == "incorrect":
                        st.markdown(f'<div class="grid-card card-incorrect">✗ {q["category"]}</div>', unsafe_allow_html=True)
                    else:
                        if st.button(q['category'].upper(), key=f"btn_{idx}", use_container_width=True):
                            st.session_state.active_idx = idx
                            st.session_state.revealed_error = False
                            st.rerun()

        st.write("---")
        correct_count = st.session_state.grid_state.count("correct")
        incorrect_count = st.session_state.grid_state.count("incorrect")
        t_col1, t_col2 = st.columns(2)
        t_col1.metric("Correct", correct_count)
        t_col2.metric("Incorrect", incorrect_count)

        if None not in st.session_state.grid_state:
            st.success("Board Cleared!")
            emojis = ['🟩' if s == 'correct' else '🟥' for s in st.session_state.grid_state]
            grid_text = f"{''.join(emojis[0:3])}\n{''.join(emojis[3:6])}\n{''.join(emojis[6:9])}"
            share_layout = f"Daily Sports Trivia ({TODAY_STR})\nScore: {correct_count}/9\n\n{grid_text}"
            st.text_area("Share your 3x3 Results Grid:", value=share_layout, height=130)
