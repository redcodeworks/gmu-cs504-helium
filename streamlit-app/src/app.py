# %%
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import streamlit as st
import eda, regression, nlp

def get_views():
    return {
        "Review Scorer": nlp,
        "Regression Analysis": regression,
        "Data Explorer": eda,
    }


def page_config():
    st.set_page_config(
        page_title="Pitchfork Review Data", layout="centered", initial_sidebar_state="auto"
    )
    st.title("Pitchfork Review Data")
    st.write("A project by Team Helium at GMU CS504")


if __name__ == "__main__":
    page_config()

    views = get_views()

    analysis_selectbox = st.sidebar.selectbox(
        "Select an analysis", list(views.keys()), index=2
    )

    page = views[analysis_selectbox]

    page.view()
