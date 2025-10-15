import streamlit as st
from datetime import datetime
import requests
from openai import OpenAI

# ---------- API initialization, pulls upcoming game from sportsDB API ----------
client = OpenAI(api_key="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")

@st.cache_data(ttl=3600)
def get_upcoming_games(sport):
    """Fetch upcoming games for the selected sport using TheSportsDB."""
    league_ids = {
        "NFL": "4391",
        "NBA": "4387",
        "MLB": "4424"
    }
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4391"
    response = requests.get(url)
    data = response.json()
    return data.get("events", [])

def analyze_upcoming_games(sport, games):
    """Generate a neutral AI summary of upcoming matchups."""
    if not games:
        return f"No upcoming {sport} games found."

    # Build a text list of upcoming games
    game_list = "\n".join(
        [f"{g['strEvent']} on {g['dateEvent']}" for g in games[:5]]
    )

    prompt = (
        f"Here are upcoming {sport} games:\n{game_list}\n\n"
        f"Write a short, neutral summary of key matchups and recent trends. "
        f"Do not include betting advice or odds."
    )

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text
    except Exception as e:
        return f"Error generating analysis: {e}"

# ---------- STREAMLIT FRONTEND ----------
sports = {
    "NFL": {"icon": "🏈", "hue": 120},
    "NBA": {"icon": "🏀", "hue": 0},
    "MLB": {"icon": "⚾", "hue": 210}
}

# Sidebar
st.sidebar.title("Select a sport!")
selected_sport = st.sidebar.selectbox("Sport:", list(sports.keys()))

# Set background colors
hue = sports[selected_sport]["hue"]
sat = 50
bg_gradient = f"linear-gradient(hsl({hue},{sat}%,15%), hsl({hue},{sat}%,25%))"
sidebar_gradient = f"linear-gradient(hsl({hue},{sat}%,20%), hsl({hue},{sat}%,30%))"

# Custom CSS
st.markdown(
    f"""
    <style>
        .stApp {{
            background: {bg_gradient};
        }}
        [data-testid="stSidebar"] > div:first-child {{
            background: {sidebar_gradient};
        }}
        .stTextInput>div>div>input {{
            background: linear-gradient(to right, #1f1f1f, #2c2c2c);
            border: 1px solid #444;
            color: #fff;
            border-radius: 12px;
            padding: 10px;
            font-size: 16px;
            transition: all 0.2s ease;
        }}
        .stTextInput>div>div>input:focus {{
            border-color: #888;
            box-shadow: 0 0 8px #555 inset;
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

# Title and date
st.title(f"BetBuddy {sports[selected_sport]['icon']}")
st.write(f"Todays Date: {datetime.now().strftime('%b %d, %Y')}")

# Chat box (optional)
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""
chat_input = st.text_input("Ask for picks or insights:", key="chat_input")

# ---------- UPCOMING GAMES + AI ANALYSIS ----------
st.subheader("Upcoming Games:")

if "selected_sport" not in st.session_state or st.session_state.selected_sport != selected_sport:
    st.session_state.selected_sport = selected_sport
    st.session_state.games = get_upcoming_games(selected_sport)
    st.session_state.analysis = analyze_upcoming_games(selected_sport, st.session_state.games)

# Show upcoming games
if st.session_state.games:
    for g in st.session_state.games[:5]:
        st.write(f"**{g['strEvent']}** — {g['dateEvent']}")
else:
    st.write("No upcoming games found.")

st.divider()
st.write("**AI Analysis:**")
st.write(st.session_state.analysis)

