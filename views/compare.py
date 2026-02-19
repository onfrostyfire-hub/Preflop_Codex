import streamlit as st

import utils


def show() -> None:
    st.subheader("Range Lab")
    db = utils.load_ranges()
    if not db:
        st.error("Нет ренджей")
        return

    source = st.selectbox("Source", list(db.keys()))
    scenario = st.selectbox("Scenario", list(db[source].keys()))
    spot = st.selectbox("Spot", list(db[source][scenario].keys()))

    st.write("### Данные спота")
    st.json(db[source][scenario][spot])
