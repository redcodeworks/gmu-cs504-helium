import streamlit as st


def view(**kwargs):

    st.write("## Data Explorer")


# %%
# states = st.multiselect("Choose states", list(states_df['state']), ['CALIFORNIA'])

# data = states_df[states_df['state'].isin(states)]
# st.write("### Population", data.sort_index())

# pop_fig = get_pop_fig(data)
# st.pyplot(pop_fig)