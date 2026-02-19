import streamlit as st

import views.compare
import views.desktop
import views.mobile
import views.stats

st.set_page_config(page_title="Preflop Trainer", layout="wide")


def main() -> None:
    st.sidebar.title("Preflop Trainer")
    mode = st.sidebar.radio("Раздел", ["🎮 Trainer", "🔬 Range Lab", "📊 Stats"])

    if mode == "🎮 Trainer":
        view = st.sidebar.radio("Вид", ["Mobile", "Desktop"], index=0)
        if view == "Mobile":
            views.mobile.show()
        else:
            views.desktop.show()
    elif mode == "🔬 Range Lab":
        views.compare.show()
    else:
        views.stats.show()


if __name__ == "__main__":
    main()
