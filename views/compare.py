import streamlit as st
import utils

def show():
    st.subheader("Range Lab")
    db = utils.load_ranges()
    if not db:
        st.warning("Нет ренджей")
        return

    source = st.selectbox("Source", list(db.keys()))
    scenario = st.selectbox("Scenario", list(db[source].keys()))
    spot = st.selectbox("Spot", list(db[source][scenario].keys()))
    data = db[source][scenario][spot]

    st.write("### Данные спота")
    st.json(data)
