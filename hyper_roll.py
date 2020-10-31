import pandas as pd
import numpy as np

from scipy.stats import hypergeom
import altair as alt
import plotly.express as px


import streamlit as st

from matrix_utils import build_univariate_transition_matrix 

def main():
    st.header("Hyper roll probablities")
    st.sidebar.title("Choose settings")

    data = pd.read_csv("tier_stats.csv", header=0, index_col=0)

    tier, level, n_champ, n_tier, gold = select_params()

    data_tier = data[str(tier)]
    draw_chart(data_tier[str(level)]/100, data_tier['pool'], n_champ,
            data_tier['N_champs']*data_tier['pool'], n_tier, gold, tier)



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
    n_champ = st.sidebar.number_input(
            'Number of cards of the same champion already bought',
            value=2, min_value=0, max_value=29)

    # Number of cards of same tier already bought
    n_tier = st.sidebar.number_input(
            'Number of cards of the same tier already bought (not including desiered champ)',
            value=25, min_value=0, max_value=300)

    # Gold
    gold = st.sidebar.number_input(
            'How much gold do you want to invert',
            value=20, min_value=1, max_value=75)
    
    return tier, level, n_champ, n_tier, gold



def draw_chart(prob_tier, N_champ, n_champ, N_tier, n_tier, gold, cost):
    # Cumulative distribution funciton
    if prob_tier>0:
        
        size = np.min((10, N_champ-n_champ+1))
        P = build_univariate_transition_matrix(N_tier-n_tier-n_champ, N_champ-n_champ, prob_tier)
                            
        P_n = [np.linalg.matrix_power(P, int(np.floor((gold-i*cost)/2))) for i in range(size)]

        prb = pd.DataFrame({
            'Proba': P_n[0][0, :],
            '1-CDF after buying': [np.sum(P_n[i][0,i:]) for i in range(size)],
            'Number of draws': [k for k in range(0, size)]
            })

        # Chart
        #st.write(prb)
        fig1 = px.bar(prb, y='Proba', x='Number of draws',
                title="Probability to find x cards if you roll for %i golds" %gold)
        fig1.update_layout(yaxis=dict(range=[0,1]), height=300)

        fig2 = px.bar(prb, y='1-CDF after buying', x='Number of draws', title="Probability to find and buy at least x cards")
        fig2.update_layout(yaxis=dict(range=[0,1]), height=300)

        st.write(fig1)
        st.write(fig2)


    else:
        st.text("You can't draw this champ !")

if __name__ == "__main__":
    main()
