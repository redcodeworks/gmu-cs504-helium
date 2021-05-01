from pickle import LIST
import streamlit as st
from data import load_review_data
import numpy as np
import altair as alt
import pandas as pd


@st.cache()
def get_review_data():
    return load_review_data()


def _filter_rows(df: pd.DataFrame, att: list, **kwargs):

    if "original_year_filter" in kwargs and kwargs["original_year_filter"]:
        df = df[
            (df["original_year"] >= kwargs["original_year_filter"][0])
            & (df["original_year"] <= kwargs["original_year_filter"][1])
        ]

    if "score_filter" in kwargs and kwargs["score_filter"]:
        df = df[
            (df["score"] >= kwargs["score_filter"][0])
            & (df["score"] <= kwargs["score_filter"][1])
        ]

    if "author_filter" in kwargs and kwargs["author_filter"]:
        df = df[df["author"] == kwargs["author_filter"]]

    if "artist_filter" in kwargs and kwargs["artist_filter"]:
        df = df[df["artist"] == kwargs["artist_filter"]]

    if df[att].dtype == "object":
        series = [""] + sorted(df[att].unique())

        return df, st.sidebar.selectbox(att, series)

    else:
        series = df[att].dropna().unique()

        min = int(series.min())
        max = int(series.max())

        return df, st.sidebar.slider(
            att,
            min,
            max,
            (min, max),
        )


def filter_df(df: pd.DataFrame) -> pd.DataFrame:

    df, original_year_filter = _filter_rows(df, "original_year")

    df, score_filter = _filter_rows(
        df, "score"  # , original_year_filter=original_year_filter
    )

    df, author_filter = _filter_rows(
        df,
        "author",
        original_year_filter=original_year_filter,
        score_filter=score_filter,
    )

    df, artist_filter = _filter_rows(
        df,
        "artist",
        pub_year_filter=original_year_filter,
        score_filter=score_filter,
        author_filter=author_filter,
    )

    df, title_filter = _filter_rows(
        df,
        "title",
        pub_year_filter=original_year_filter,
        score_filter=score_filter,
        author_filter=author_filter,
        artist_filter=artist_filter,
    )

    return df


def display_reissues(df: pd.DataFrame) -> pd.DataFrame:

    mode = st.sidebar.radio("Show Reissues", ["yes", "no", "only"])

    if mode == "yes":
        return df

    elif mode == "no":
        return df[df["reissue"] == 0]

    elif mode == "only":
        return df[df["reissue"] == 1]


def select_summary_attributes(df: pd.DataFrame):
    return st.multiselect(
        "Choose Attributes",
        list(df.columns),
        ["original_year", "artist", "title", "best_new_music", "reissue"],
    )


def write_preview(df: pd.DataFrame, atts: list):
    col1, col2, col3 = st.beta_columns(3)

    col1.write("#### Total Rows")
    col1.write(df.shape[0])

    col2.write("#### Total Columns")
    col2.write(df.shape[1])

    top = col3.number_input("Show Top N Results", min_value=1, value=255)

    st.dataframe(df[atts + ["score"]].head(top))


def write_summary_statistics(df: pd.DataFrame):
    st.write("### Sumary Statistics")

    st.dataframe(df[["score"]].describe().T)


def write_histogram(df: pd.DataFrame):
    st.write("### Histogram")

    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("score:Q", bin=alt.Bin(maxbins=100)),
            alt.Y("count()"),
            # alt.Color("reissue:N")
        )
        .properties(width=700)
    )


def write_bar_chart(df: pd.DataFrame):

    st.write("### Counts and Average Score")

    x = st.selectbox(
        "Series", ["original_year:O", "pub_year:O", "reissue:N"]
    )

    base = alt.Chart(df).encode(x=alt.X(x))
    bar = base.mark_bar().encode(
        y=alt.Y("count()", axis=alt.Axis(title="Count of Reviews", titleColor="blue"))
    )
    line = base.mark_line(color="red").encode(
        y=alt.Y(
            "average(score)", axis=alt.Axis(title="Average Score", titleColor="red")
        )
    )
    chart = alt.layer(bar, line).resolve_scale(y="independent").properties(width=700)

    st.altair_chart(chart)


def view(**kwargs):

    df = get_review_data()

    df = filter_df(df)
    df = display_reissues(df)

    atts = select_summary_attributes(df)

    st.write("## Data Explorer")
    write_preview(df, atts)

    write_summary_statistics(df)

    write_histogram(df)

    write_bar_chart(df)
