from collections import Counter

import streamlit as st
import SessionState

ORDER = 0
PLAYERS = {}

@st.cache(allow_output_mutation=True)
def set_default_players(players):
    global PLAYERS
    PLAYERS = {s: 'alive' for s in players}
    return PLAYERS

def page_layout(players):
    st.text("\n")
    st.text("\n")
    st.text('Note: This tool is only useful when everyone is still alive. Indeed, you are assured to play one of the 3 players you least recently played.')
    st.text("\n")
    st.text("\n")
    left, right = st.beta_columns(2)
    if not all(players):
        st.subheader("Please enter every player name in the sidebar.")
    else:
        with left:
            st.subheader("Which player have you faced this round?")
        with right:
            st.subheader("Which player can you face next?")
        st.text("\n")
        st.text("\n")


def main():
    global ORDER
    global PLAYERS

    st.sidebar.title("Lobby player names")

    players = []
    for i in range(1, 8):
        players.append(st.sidebar.text_input(f'Player {i}', max_chars=20, value=f''))

    set_default_players(players)

    ss = None

    page_layout(players)
    if not all(players):
        return

    left_1, left_2, center, right = st.beta_columns([0.2, 0.2, 5, 1])

    alive_players = [k for k in PLAYERS if PLAYERS[k] == 'alive']
    states = {s: 0 for s in alive_players}

    print(alive_players)
    for index, p in enumerate(alive_players):
        if p in alive_players:
            with left_1:
                if st.button(p, key=index):  # summoner name was clicked
                    ss = SessionState.get(**states)
                    ORDER += 1
                    setattr(ss, p, ORDER)
        with left_2:
            if st.button('X', key=index*2):
                PLAYERS[p] = 'dead'
                ss = SessionState.get(**states)
                delattr(ss, p)
                for p in alive_players:
                    setattr(ss, p, 0)


    with center:
        if st.button('Reset matchmaking'):
            ss = SessionState.get(**states)
            old_names = [s for s in ss.__dict__]  # remove old names if text inputs changed in sidebar
            for name in old_names:
                delattr(ss, name)
            for p in players:
                setattr(ss, p, 0)
            ORDER = 0

    if not ss:
        return

    counter = Counter(ss.__dict__)

    not_matched_yet = [s[0] for s in counter.items() if s[1] == 0]
    can_match = [c[0] for c in counter.most_common()[:-4:-1]]  # 3 players least recently played

    possibilities = set(not_matched_yet) | set(can_match)

    with right:
        for p in possibilities:
            st.markdown(f'- **{p}**')

