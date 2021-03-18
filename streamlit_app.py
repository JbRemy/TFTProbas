from helpers import *

# Importing pages
import roll
import chosen_roll
import matchmaking


PAGES = {
    "Roll": roll,
    "Chosen Roll": chosen_roll,
    # "Matchmaking": matchmaking,
}

st.set_page_config(page_title='TFT tools', page_icon='assets/fob_legend.jpg', layout='wide', initial_sidebar_state='auto')
tft_image = st.sidebar.image("assets/tft_fob.png", width=300)
st.header("Teamfight Tactics tools - Set 4.5")
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

github_repo = get_img_with_href('assets/github.png', 'https://github.com/sde-cdsp/TFTProbas', text="Project: ")
credits = "by [LittleToof](https://twitter.com/Toof_pro) & [Pas De Bol](https://twitter.com/PasDeBolTFT)"

left, right = st.beta_columns(2)
with left:
    st.markdown(github_repo, unsafe_allow_html=True)
with right:
    st.markdown(credits, unsafe_allow_html=True)

left, right = st.beta_columns(2)

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.main()
