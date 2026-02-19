import streamlit as st

import utils
from spot_config import get_spot_config


def show() -> None:
    st.subheader("Trainer • Desktop")
    ranges_db = utils.load_ranges()
    if not ranges_db:
        st.error("Нет ренджей в папке ranges_spots")
        return

    source = st.selectbox("Source", list(ranges_db.keys()), key="d_source")
    scenarios = list(ranges_db[source].keys())
    chosen_scenarios = st.multiselect("Scenario", scenarios, default=scenarios, key="d_scenarios")

    filters = ["All"] + list(utils.GROUPS_DEFINITIONS.keys())
    all_spots = sorted({s for sc in chosen_scenarios for s in ranges_db[source][sc].keys()})
    filters.extend(all_spots)
    filter_mode = st.selectbox("Фильтр", filters, key="d_filter")

    if st.button("🎲 Новая рука", key="d_new") or "d_task" not in st.session_state:
        task = utils.choose_random_task(ranges_db, source, chosen_scenarios, filter_mode)
        if task is None:
            st.warning("Под фильтр ничего не найдено")
            return
        st.session_state["d_task"] = task
        st.session_state["d_answer"] = None

    task = st.session_state["d_task"]
    cfg = get_spot_config(task["spot"])

    st.write(f"**Spot:** {task['spot']}")
    st.write(f"**Hero:** {cfg.hero} | **Villain:** {cfg.villain or '-'} | **Dealer:** {cfg.dealer}")
    st.code(f"Hand: {task['hand']} | RNG: {task['rng']}")

    c1, c2, c3 = st.columns(3)
    if c1.button("FOLD", key="d_fold"):
        st.session_state["d_answer"] = "FOLD"
    if c2.button("CALL", key="d_call"):
        st.session_state["d_answer"] = "CALL"
    if c3.button("BET", key="d_bet"):
        if task["correct"] == "3BET":
            st.session_state["d_answer"] = "3BET"
        elif task["correct"] == "4BET":
            st.session_state["d_answer"] = "4BET"
        else:
            st.session_state["d_answer"] = "RAISE"

    answer = st.session_state.get("d_answer")
    if answer:
        is_ok = answer == task["correct"]
        utils.save_to_history(task["spot"], task["hand"], 1 if is_ok else 0, task["correct"])
        if is_ok:
            st.success(f"Верно: {task['correct']}")
        else:
            st.error(f"Неверно. Правильно: {task['correct']}")

        with st.expander("Показать ренджи"):
            st.json(task["data"])
