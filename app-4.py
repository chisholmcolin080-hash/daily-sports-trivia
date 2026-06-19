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
        {"id": 0, "category": "Career Path", "question": "Who is this? Jets-Panthers-Cardinals-Dolphins-Commanders", "answer": "Robbie Chosen"},
        {
            "id": 1, 
            "category": "Guess who", 
            "question": "Who is pictured here?", 
            "answer": "Mitch Moreland", 
            # High-speed public CDN image link that bypasses all security restrictions
            "image_url": "https://cdn.mlbtraderumors.com/files/2014/11/USATSI_7950726_154513410_lowres.jpg"
        },
        {"id": 2, "category": "Who is #1", "question": "Since 2000, what guardians pitcher has the most pitching strikeouts with 1,461?", "answer": "Corey Kluber"},
        {"id": 3, "category": "College Sports", "question": "This past season in CBB saw Braden Smith break whose assists record?", "answer": "Bobby Hurley"},
        {"id": 4, "category": "Awards", "question": "What NHL award is the oldest? (Three words)", "answer": "Hart Memorial Trophy"},
        {"id": 5, "category": "Playoffs", "question": "In 2016, what golfer choked a 5 shot lead heading into the final 9 holes?", "answer": "Jordan Spieth"},
        {"id": 6, "category": "Draft", "question": "What florida state player has the most sacks from the 2019 NFL draft class with 71?", "answer": "Brian Burns"},
        {"id": 7, "category": "Championships", "question": "Since 1990, four NHL players are tied with 4 stanley cups with three coming from the blackhawks. Who is the one player not from the Blackhawks with 4?", "answer": "Chris Kunitz"},
        {"id": 8, "category": "Connect them", "question": "What teammate connects Patrick Mahomes with Spencer Rattler (Offensive Skill Position)?", "answer": "Clyde Edwards-Helaire"}
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
