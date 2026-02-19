import streamlit as st

import utils


def show() -> None:
    st.subheader("Stats")
    df = utils.load_history()

    if df.empty:
        st.info("История пока пустая")
        return

    total = len(df)
    correct = int(df["Result"].sum())
    acc = int((correct / total) * 100) if total else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Всего рук", total)
    c2.metric("Верных", correct)
    c3.metric("Точность", f"{acc}%")

    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)

    if st.button("Очистить историю"):
        utils.delete_history(days=None)
        st.success("История очищена")
