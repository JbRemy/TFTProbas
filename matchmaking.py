from collections import Counter

import streamlit as st
import SessionState

ORDER = 0

def page_layout(summoners):
    st.text("\n")
    st.text("\n")
    st.text('Note: This tool is only useful when everyone is still alive. Indeed, you are assured to play one of the 3 players you least recently played.')
    st.text("\n")
    st.text("\n")
    left, right = st.beta_columns(2)
    if not all(summoners):
        st.subheader("Please enter every summoner name in the sidebar.")
    else:
        with left:
            st.subheader("Which player have you played against this round?")
        with right:
            st.subheader("Which player can you play against next?")
        st.text("\n")
        st.text("\n")


def main():
    global ORDER
    st.sidebar.title("Lobby summoner names")

    summoners = []
    for i in range(1, 8):
        summoners.append(st.sidebar.text_input(f'Summoner {i}', max_chars=20, value=f''))
    states = {s: 0 for s in summoners}
    ss = None

    page_layout(summoners)
    if not all(summoners):
        return

    left, right = st.beta_columns(2)

    with left:
        for index, s in enumerate(summoners):
            if st.button(s, key=index):  # summoner name was clicked
                if ss is None:  # button clicked for first time
                    ss = SessionState.get(**states)
                ORDER += 1
                setattr(ss, s, ORDER)

    if ss is None:
        return
    counter = Counter(ss.__dict__)

    not_matched_yet = [s[0] for s in counter.items() if s[1] == 0]
    can_match = [c[0] for c in counter.most_common()[:-4:-1]]  # 3 players least recently played

    possibilities = set(not_matched_yet) | set(can_match)

    with right:
        st.markdown('You can fight:\n')
        for p in possibilities:
            st.markdown(f'- **{p}**')

