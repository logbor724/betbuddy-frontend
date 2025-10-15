import streamlit as st
from datetime import datetime  # to show current date

# assigns each sport a different color for the sidebar and bg
sports = {
    "NFL": {"icon": "🏈", "hue": 120},
    "NBA": {"icon": "🏀", "hue": 0},
    "MLB": {"icon": "⚾", "hue": 210}
}

# sidebar lets user select sport
st.sidebar.title("Select a sport!")
selected_sport = st.sidebar.selectbox("Sport:", list(sports.keys()))  # dropdown for sports

# gradient colors for page and sidebar using same brightness
hue = sports[selected_sport]["hue"]  # get hue based on selected sport
sat = 50  # saturation of color

# bg and sidebar gradient strings
bg_gradient = f"linear-gradient(hsl({hue},{sat}%,15%), hsl({hue},{sat}%,25%))"
sidebar_gradient = f"linear-gradient(hsl({hue},{sat}%,20%), hsl({hue},{sat}%,30%))"

# apply styling with css
st.markdown(
    f"""
    <style>
        .stApp {{
            background: {bg_gradient};  # main page background
        }}
        [data-testid="stSidebar"] > div:first-child {{
            background: {sidebar_gradient};  # sidebar background
        }}
        .stTextInput>div>div>input {{
            background: linear-gradient(to right, #1f1f1f, #2c2c2c);  # subtle dark gradient
            border: 1px solid #444;  # darker border so not harsh
            color: #fff;  # white text
            border-radius: 12px;  # more rounded corners
            padding: 10px;  # inner spacing
            font-size: 16px;  # slightly bigger text
            transition: all 0.2s ease;  # smooth hover/focus effect
        }}
        .stTextInput>div>div>input:focus {{
            border-color: #888;  # highlight border when typing
            box-shadow: 0 0 8px #555 inset;  # subtle inner glow
        }}
        .stButton>button {{
            background-color: #555; 
            color: #fff;
            border-radius: 6px;
            padding: 5px 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title(f"BetBuddy {sports[selected_sport]['icon']}")  # shows name with icon

st.write(f"Todays Date: {datetime.now().strftime('%b %d')}, {datetime.now().strftime('%Y')}")  # format like Oct 13, 2025

# chat input box for user
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""  # initialize session state if not exist

chat_input = st.text_input("Ask for picks:", key="chat_input")  # input box for questions

# upcoming games placeholder section
st.subheader("Upcoming Games:")  # header for upcoming games
st.write(f"here would be the upcoming {selected_sport} games if yall wanna add that")  # placeholder text