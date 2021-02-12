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
    link = '[Repo](https://github.com/sde-cdsp/TFTProbas) (credit: [JBRemy](https://github.com/JBRemy))'
    st.markdown(link, unsafe_allow_html=True)
    # st.write('')
    st.header("Roll probabilities")
    st.sidebar.title("Choose settings")

    data = pd.read_csv("tier_stats.csv", header=0, index_col=0)

    tier, level, n_champ, n_tier, gold = select_params()

    data_tier = data[str(tier)]
    draw_chart(data_tier[str(level)] / 100, data_tier['pool'], n_champ,
               data_tier['N_champs'] * data_tier['pool'], n_tier, gold, tier)


def select_params():
    # Champion Tier
    tier = st.sidebar.selectbox(
        'Select the champion tier',
        (1, 2, 3, 4, 5)
    )
    # Level
    level = st.sidebar.slider(
        'Select your level', value=5,
        min_value=1, max_value=9, step=1)

    # Number of cards of the champion already bought
    n_champ = st.sidebar.number_input(
        'Number of copies of the champion already out',
        value=2, min_value=0, max_value=29)

    # Number of cards of same tier already bought
    n_tier = st.sidebar.number_input(
        f'Number of {tier} cost champions already out (excluding your champion)',
        value=25, min_value=0, max_value=300)

    # Gold
    gold = st.sidebar.number_input(
        'How much gold to roll',
        value=20, min_value=1, max_value=100)

    return tier, level, n_champ, n_tier, gold


def draw_chart(prob_tier, N_champ, n_champ, N_tier, n_tier, gold, cost):
    # Cumulative distribution function
    if prob_tier > 0:

        size = np.min((10, N_champ - n_champ + 1))
        P = build_univariate_transition_matrix(N_tier - n_tier - n_champ, N_champ - n_champ, prob_tier)

        P_n = [np.linalg.matrix_power(P, int(np.floor((gold - i * cost) / 2))) for i in range(size)]
        # print(P_n)
        prb = pd.DataFrame({
            'Proba': P_n[0][0, :][1:],
            'Probability': pd.Series([np.sum(P_n[i][0, i:]) * 100 for i in range(size)][1:]).round(2),
            'Number of copies': [k for k in range(1, size)]
        })

        # Chart
        # st.write(prb)

        # fig1 = px.bar(prb, y='Proba', x='Number of draws',
        #         title="Probability to find x copies if you roll %i golds" %gold)
        # fig1.update_layout(yaxis=dict(range=[0,100]), height=300)

        fig2 = px.bar(prb, y='Probability', x='Number of copies', title="Probability to draw your champion",
                      text='Probability')
        fig2.update_layout(yaxis=dict(range=[0, 100]), height=600, width=1000, xaxis={'tickmode': 'linear'})
        fig2.update_traces(hovertemplate="At least %{x}: <b>%{y:.2f}</b> %<br><extra></extra>",
                           texttemplate='<b>%{text:.2f}</b> %', textposition='outside')

        # st.write(fig1)
        st.write(fig2)


    else:
        st.text("You can't draw this champ !")


if __name__ == "__main__":
    main()
