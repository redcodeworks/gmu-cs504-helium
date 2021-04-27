# %%
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import exploration, regression, nlp

def get_views():
    return {
        "Review Scorer": nlp,
        "Regression Analysis": regression,
        "Data Explorer": exploration,
    }

views = get_views()

# %%
st.title("Pitchfork Review Data")
st.write("A project by Team Helium at GMU CS504")


analysis_selectbox = st.sidebar.selectbox(
    "Select an analysis", list(views.keys()), index=0
)



page = views[analysis_selectbox]

page.view()
