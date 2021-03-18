import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import json

from helpers import roll_page_layout
from matrix_utils import build_univariate_transition_matrix

def main():
    roll_page_layout()

    data = pd.read_csv("tier_stats.csv", header=0, index_col=0)
    chosen_data = pd.read_csv("chosen_tier_stats.csv", header=0, index_col=0)

    with open('champions.json', 'r') as file:
        traits = pd.DataFrame(json.load(file))

    tier, tot_n_traits, level, n_champ, n_tier, n_traits, gold = select_params(data, traits)

    data_tier = data[str(tier)]
    chosen_data_tier = data[str(tier)]

    prob = (n_traits/tot_n_traits)*(chosen_data_tier[str(level)] / 100)
    draw_chart(prob, data_tier['pool'], n_champ,
               data_tier['N_champs'] * data_tier['pool'], n_tier, gold, tier)


def select_params(data, traits):
    # Champion 
    champ_name = st.sidebar.selectbox(
        'Select the champion tier',
        list(traits.name),
    )
    
    tier = traits.loc[traits.name==champ_name, 'cost'].item()
    tot_n_traits = len(traits.loc[traits.name==champ_name, 'traits'].item())

    # Level
    level = st.sidebar.selectbox(
        'Select your level',
        tuple(range(1, 10)),
        index=7,
    )

    # Number of cards of the champion already bought
    nb_copies = data[str(tier)]['pool']
    n_champ = st.sidebar.number_input(
        'Number of copies of the champion already out',
        value=3, min_value=0, max_value=nb_copies)

    # Number of cards of same tier already bought
    n_tier = st.sidebar.number_input(
        f'Number of {tier} cost champions already out (excluding your champion)',
        value=25, min_value=0, max_value=300)

    # Number of traits requiered
    n_traits = st.sidebar.number_input(
        f'Number of interesting traits',
        value=1, min_value=1, max_value=3)

    # Gold
    gold = st.sidebar.number_input(
        'How much gold to roll',
        value=50, min_value=1, max_value=100)

    return tier, tot_n_traits, level, n_champ, n_tier, n_traits, gold


def draw_chart(prob_tier, N_champ, n_champ, N_tier, n_tier, gold, cost):
    # Cumulative distribution function
    if prob_tier > 0:

        P = (N_champ - n_champ)/(N_tier - n_tier - n_champ)*0.5*prob_tier
        print(P)

        P_n = [(1-(1 - P)**i)*100 for i in range(1,int(np.floor((gold - cost) / 2))+1)]
        prb = pd.DataFrame({
            'Probability': pd.Series(P_n),
            'Number of rolls': [i for i in range(1,int(np.floor((gold - cost) / 2))+1)]
        })

        fig2 = px.bar(prb, y='Probability', x='Number of rolls', title="Odds to find your chosen champion",
                      text='Probability')
        fig2.update_layout(yaxis=dict(range=[0, 100]), height=600, width=1000, xaxis={'tickmode': 'linear'})
        fig2.update_traces(hovertemplate="At least %{x}: <b>%{y:.2f}</b> %<br><extra></extra>",
                           texttemplate='<b>%{text:.2f}</b> %', textposition='outside')

        st.write(fig2)

    else:
        st.text("You can't find this champion with these settings!")
