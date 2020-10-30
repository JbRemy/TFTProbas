import pandas as pd
import numpy as np
from scipy.stats import hypergeom
import altair as alt

import streamlit as st

def main():
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Exploration"])
    st.header("High roll probablities")
    st.sidebar.title("Choose settings")

    data = pd.read_csv("tier_stats.csv", header=0, index_col=0)

    tier, level, n_champ, n_tier, gold = select_params()

    data_tier = data[str(tier)]
    draw_chart(data_tier[str(level)]/100, data_tier['pool'], n_champ,
            data_tier['N_champs']*data_tier['pool'], n_tier, gold)



def select_params():
    # Champion Tier
    tier = st.sidebar.selectbox(
            'Select a champion tier',
            (1,2,3,4,5)
            )
    # Level
    level = st.sidebar.slider(
            'Select your little legend level', value=5,
                min_value=1, max_value=9, step=1)

    # Number of cards of the champion already bought
    n_champ = st.sidebar.slider(
            'Number of cards of the same champion already bought',
            value=2, min_value=0, max_value=29, step=1)

    # Number of cards of same tier already bought
    n_tier = st.sidebar.slider(
            'Number of cards of the same tier already bought (not including desiered champ)',
            value=25, min_value=0, max_value=300, step=1)

    # Gold
    gold = st.sidebar.slider(
            'How much gold do you want to invert',
            value=20, min_value=1, max_value=75, step=1)
    
    return tier, level, n_champ, n_tier, gold



def draw_chart(prob_tier, N_champ, n_champ, N_tier, n_tier, gold):
    # Cumulative distribution funciton
    if prob_tier>0:
        prb = pd.DataFrame({
            'Proba': [1 - hypergeom.cdf(k, 
                np.int((N_tier-n_tier-n_champ)/prob_tier),
                (N_champ-n_champ),
                np.int(5*gold/2)) for k in range(0,10)],
            'Number of draws': [k for k in range(0,10)]
            })

        # Chart
        st.write(prb)
        st.write(alt.Chart(prb).mark_bar().encode(
                x='Number of draws',
                y='Proba',
            ))
    else:
        st.text("You can't draw this champ !")

if __name__ == "__main__":
    main()
