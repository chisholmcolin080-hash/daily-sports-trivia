import streamlit as st
from datetime import date

st.set_page_config(page_title="Daily Sports Trivia", layout="centered")

# Custom CSS to force clean squares and mimic a sports dashboard
st.markdown("""
    <style>
    .stApp { background-color: #0b1329; color: white; }
    .game-title { color: #facc15; font-family: 'Arial Black', sans-serif; font-style: italic; font-weight: 900; text-align: center; font-size: 42px; margin-bottom: 0px; }
    .game-subtitle { color: #94a3b8; font-family: sans-serif; text-align: center; font-size: 14px; margin-top: 5px; margin-bottom: 30px; }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 30px;
    }

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

TODAY_STR = str(date.today())
DAILY_TRIVIA = {
    TODAY_STR: [
        {"id": 0, "category": "NFL", "question": "Which team won the very first Super Bowl?", "answer": "Packers", "image_url": ""},
        # Verified public photo link that will load cleanly
        {"id": 1, "category": "NBA", "question": "Who is pictured handling the ball here?", "answer": "LeBron James", "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=500"}, 
        {"id": 2, "category": "MLB", "question": "Which team plays their home games at Fenway Park?", "answer": "Red Sox", "image_url": ""},
        {"id": 3, "category": "College Football", "question": "What school uses the 'Block O' logo?", "answer": "Ohio State", "image_url": ""},
        {"id": 4, "category": "World Cup", "question": "Which country won the 2022 FIFA World Cup?", "answer": "Argentina", "image_url": ""},
        {"id": 5, "category": "NHL", "question": "What trophy is awarded to the NHL playoff champion?", "answer": "Stanley Cup", "image_url": ""},
        {"id": 6, "category": "Golf", "question": "How many major championships has Tiger Woods won?", "answer": "15", "image_url": ""},
        {"id": 7, "category": "Tennis", "question": "Which Grand Slam tournament is played on grass courts?", "answer": "Wimbledon", "image_url": ""},
        {"id": 8, "category": "UFC", "question": "What is the nickname of fighter Conor McGregor?", "answer": "The Notorious", "image_url": ""}
    ]
}

questions = DAILY_TRIVIA.get(TODAY_STR, [])

if not questions:
    st.error("No Sports Trivia loaded for today's date yet!")
else:
    if 'grid_state' not in st.session_state:
        st.session_state.grid_state = [None] * 9
    if 'active_idx' not in st.session_state:
        st.session_state.active_idx = None

    st.markdown('<h1 class="game-title">DAILY SPORTS TRIVIA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">Daily Trivia Board — ' + TODAY_STR + '</p>', unsafe_allow_html=True)

    # VIEW A: Individual Question Display
    if st.session_state.active_idx is not None:
        idx = st.session_state.active_idx
        q_data = questions[idx]

        st.subheader(f"Category: {q_data['category']}")

        # Display photo if the link is populated
        if q_data.get("image_url"):
            st.image(q_data["image_url"], use_container_width=True)

        st.write(f"### {q_data['question']}")

        # Notice to players that spelling and capitalization matter
        user_guess = st.text_input("Type your answer:", key="guess_input", placeholder="Exact spelling & capitalization required...")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Guess", type="primary"):
                if user_guess:
                    # STRICT SPELLING ENFORCEMENT: Direct comparison without flattening string cases
                    if user_guess == q_data['answer']:
                        st.session_state.grid_state[idx] = "correct"
                    else:
                        st.session_state.grid_state[idx] = "incorrect"

                    st.session_state.active_idx = None
                    st.rerun()
        with col2:
            if st.button("Back to Board"):
                st.session_state.active_idx = None
                st.rerun()

    # VIEW B: Base Grid Selection View
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
