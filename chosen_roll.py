import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import json
from collections import Counter

from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helpers import roll_page_layout
from matrix_utils import build_univariate_transition_matrix


def main():
    roll_page_layout()

    data = pd.read_csv("tier_stats.csv", header=0, index_col=0)
    chosen_data = pd.read_csv("chosen_tier_stats.csv", header=0, index_col=0)

    with open('champions.json', 'r') as file:
        traits = pd.DataFrame(json.load(file))

    names, tiers, trait_ratio, level, n_champs, n_tiers = select_params(data, chosen_data, traits)

    if not names:
        st.subheader("Select champion(s) in the sidebar")
        return

    probs = []
    for tier, n_champ, n_tier, ratio in zip(tiers, n_champs, n_tiers, trait_ratio):
        data_tier = data[str(tier)]
        prob = ratio * (chosen_data.iloc[level - 1][tier - 1] / 100)
        probs.append(
            (data_tier['pool'] - n_champ) / (data_tier['N_champs'] * data_tier['pool'] - n_tier - n_champ) * 0.5 * prob)

    draw_chart(probs, names)


def select_params(data, chosen_data, traits):
    # Level
    level = st.sidebar.selectbox(
        'Select your level',
        tuple(range(1, 10)),
        index=7,
    )
    chosen_odds = list(chosen_data.iloc[level - 1])
    available_costs = [i + 1 for i in range(5) if chosen_odds[i] > 0]
    available_traits = traits[traits['cost'].isin(available_costs)]

    champs = st.sidebar.multiselect(
        'Select the champions',
        build_champ_select(available_traits, level),
    )
    champions = [champ.split(' - ')[0] for champ in champs]

    names, tiers, traits_ratio = build_champ_info(champions, available_traits)

    n_champs = []
    for champ, tier in zip(names, tiers):
        # Number of cards of the champion already bought
        nb_copies = data[str(tier)]['pool']
        n_champs.append(st.sidebar.number_input(
            'Number of copies of %s already out' % champ,
            value=3, min_value=0, max_value=nb_copies))

    n_tiers = {}
    for tier in np.unique(tiers):
        # Number of cards of same tier already bought
        n_tiers[str(tier)] = st.sidebar.number_input(
            f'Number of {tier} cost champions already out (excluding your champion)',
            value=25, min_value=0, max_value=300)

    n_tiers = [n_tiers[str(tier)] for tier in tiers]

    return names, tiers, traits_ratio, level, n_champs, n_tiers


def draw_chart(probs, names):
    prob = np.prod([1 - p for p in probs])
    prb = pd.DataFrame({
        'Probability': pd.Series([(1 - prob ** i) * 100 for i in range(1, 51)]),
        'Golds spent': [i for i in range(2, 102, 2)]
    })

    fig = px.line(prb, y='Probability', x='Golds spent', title="Odds to find one of the desired chosen",
                  text='Probability')
    fig.update_layout(yaxis=dict(range=[0, 100]), height=600, width=1000,
                      xaxis={'tickmode': 'linear', 'dtick': 4, 'range': [0, 100]}, hovermode='x')
    fig.update_traces(hovertemplate="Probability: <b>%{y:.2f}</b>%<br>Golds spent: <b>%{x}</b>", text='', mode='lines')

    st.write(fig)

    rows = int(len(names) / 2 + 1)
    cols = 2
    traces = []
    for i, (prob, name) in enumerate(zip(probs, names)):
        prb = pd.DataFrame({
            'Probability': pd.Series([(1 - (1 - prob) ** i) * 100 for i in range(1, 51)]),
            'Golds spent': [i for i in range(2, 102, 2)]
        })
        row = int((i + 2) / 2)
        col = 1 if i % 2 == 0 else 2
        fig = px.line(prb, y='Probability', x='Golds spent',
                      title="Odds to find a chosen %s with desired traits" % name, text='Probability')
        trace = fig['data'][0]
        traces.append((trace, row, col))

    fig2 = make_subplots(rows=rows, cols=cols, subplot_titles=names)
    for trace in traces:
        fig2.add_trace(trace[0], row=trace[1], col=trace[2])
    fig2.update_layout(height=600 * rows, width=1000, hovermode='x')
    fig2.update_xaxes(title_text="Golds spent")
    fig2.update_yaxes(title_text="Probability", range=[0, 100])
    fig2.update_traces(hovertemplate="Probability: <b>%{y:.2f}</b>%<br>Golds spent: <b>%{x}</b>", text='', mode='lines')

    st.write(fig2)


def build_champ_select(traits, level):
    out = []
    for row in traits.iterrows():
        for trait in row[1]['chosen_traits']:
            out.append(row[1]['name'] + ' - ' + trait)

    return out


def build_champ_info(champions, traits):
    names = []
    tiers = []
    traits_ratio = []

    for champ, count in Counter(champions).items():
        names.append(champ)
        tiers.append(traits.loc[traits.name == champ, 'cost'].item())
        traits_ratio.append(count / len(traits.loc[traits.name == champ, 'chosen_traits'].item()))

    return names, tiers, traits_ratio
