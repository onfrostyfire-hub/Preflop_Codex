import streamlit as st

import utils
from spot_config import get_spot_config


def show() -> None:
    st.subheader("Trainer • Mobile")
    ranges_db = utils.load_ranges()
    if not ranges_db:
        st.error("Нет ренджей в папке ranges_spots")
        return

    source = st.selectbox("Source", list(ranges_db.keys()), key="m_source")
    scenarios = list(ranges_db[source].keys())
    chosen_scenarios = st.multiselect("Scenario", scenarios, default=scenarios, key="m_scenarios")

    filters = ["All"] + list(utils.GROUPS_DEFINITIONS.keys())
    all_spots = sorted({s for sc in chosen_scenarios for s in ranges_db[source][sc].keys()})
    filters.extend(all_spots)
    filter_mode = st.selectbox("Фильтр", filters, key="m_filter")

    if st.button("🎲 Новая рука", key="m_new") or "m_task" not in st.session_state:
        task = utils.choose_random_task(ranges_db, source, chosen_scenarios, filter_mode)
        if task is None:
            st.warning("Под фильтр ничего не найдено")
            return
        st.session_state["m_task"] = task
        st.session_state["m_answer"] = None

    task = st.session_state["m_task"]
    cfg = get_spot_config(task["spot"])

    st.write(f"**Spot:** {task['spot']}")
    st.write(f"**Hero:** {cfg.hero} | **Villain:** {cfg.villain or '-'} | **Dealer:** {cfg.dealer}")
    st.code(f"Hand: {task['hand']} | RNG: {task['rng']}")

    c1, c2, c3 = st.columns(3)
    if c1.button("FOLD", key="m_fold"):
        st.session_state["m_answer"] = "FOLD"
    if c2.button("CALL", key="m_call"):
        st.session_state["m_answer"] = "CALL"
    if c3.button("BET", key="m_bet"):
        if task["correct"] == "3BET":
            st.session_state["m_answer"] = "3BET"
        elif task["correct"] == "4BET":
            st.session_state["m_answer"] = "4BET"
        else:
            st.session_state["m_answer"] = "RAISE"

    answer = st.session_state.get("m_answer")
    if answer:
        is_ok = answer == task["correct"]
        utils.save_to_history(task["spot"], task["hand"], 1 if is_ok else 0, task["correct"])
        if is_ok:
            st.success(f"Верно: {task['correct']}")
        else:
            st.error(f"Неверно. Правильно: {task['correct']}")

        with st.expander("Показать ренджи"):
            st.json(task["data"])
