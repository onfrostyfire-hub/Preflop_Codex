import streamlit as st
import utils

def show():
    st.subheader("Stats")
    db = utils.load_ranges()
    if not db:
        st.warning("Нет ренджей")
        return

    total_sources = len(db)
    total_scenarios = sum(len(db[s]) for s in db)
    total_spots = sum(len(db[s][sc]) for s in db for sc in db[s])

    st.write(f"Sources: **{total_sources}**")
    st.write(f"Scenarios: **{total_scenarios}**")
    st.write(f"Spots: **{total_spots}**")
