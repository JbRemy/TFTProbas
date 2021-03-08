import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from matrix_utils import build_univariate_transition_matrix


def main():
    st.markdown(
        f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: {1200}px;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )
    link = "[Repo](https://github.com/sde-cdsp/TFTProbas) (credit: [JBRemy](https://github.com/JBRemy))"
    left, right = st.beta_columns(2)
    with left:
        st.markdown(link, unsafe_allow_html=True)
    with right:
        st.text("Patch 11.5")
    st.header("Roll probabilities")
    st.sidebar.title("Settings")

    data = pd.read_csv("tier_stats.csv", header=0, index_col=0)

    tier, level, n_champ, n_tier, gold = select_params(data)

    data_tier = data[str(tier)]

    draw_chart(data_tier[str(level)] / 100, data_tier['pool'], n_champ,
               data_tier['N_champs'] * data_tier['pool'], n_tier, gold, tier)


def select_params(data):
    # Champion Tier
    tier = st.sidebar.selectbox(
        'Select the champion tier',
        tuple(range(1, 6)),
        index=3,
    )
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
        value=0, min_value=0, max_value=nb_copies)

    # Number of cards of same tier already bought
    n_tier = st.sidebar.number_input(
        f'Number of {tier} cost champions already out (excluding your champion)',
        value=25, min_value=0, max_value=300)

    # Gold
    gold = st.sidebar.number_input(
        'How much gold to roll',
        value=50, min_value=1, max_value=100)

    return tier, level, n_champ, n_tier, gold


def draw_chart(prob_tier, N_champ, n_champ, N_tier, n_tier, gold, cost):
    # Cumulative distribution function
    if prob_tier > 0:

        size = np.min((10, N_champ - n_champ + 1))
        P = build_univariate_transition_matrix(N_tier - n_tier - n_champ, N_champ - n_champ, prob_tier)

        P_n = [np.linalg.matrix_power(P, int(np.floor((gold - i * cost) / 2))) for i in range(size)]
        prb = pd.DataFrame({
            'Proba': P_n[0][0, :][1:],
            'Probability': pd.Series([np.sum(P_n[i][0, i:]) * 100 for i in range(size)][1:]).round(2),
            'Number of copies': [k for k in range(1, size)]
        })

        fig2 = px.bar(prb, y='Probability', x='Number of copies', title="Probability to draw your champion",
                      text='Probability')
        fig2.update_layout(yaxis=dict(range=[0, 100]), height=600, width=1000, xaxis={'tickmode': 'linear'})
        fig2.update_traces(hovertemplate="At least %{x}: <b>%{y:.2f}</b> %<br><extra></extra>",
                           texttemplate='<b>%{text:.2f}</b> %', textposition='outside')

        st.write(fig2)


    else:
        st.text("You can't draw this champ !")


if __name__ == "__main__":
    main()
