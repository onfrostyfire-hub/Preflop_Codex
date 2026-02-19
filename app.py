import streamlit as st
import views.mobile
import views.desktop
import views.compare
import views.stats

st.set_page_config(page_title="Preflop Trainer", layout="wide")

def main():
    with st.sidebar:
        st.title("Preflop Trainer")
        mode = st.radio("Раздел", ["🎮 Trainer", "🔬 Range Lab", "📊 Stats"])
        view = st.radio("Вид", ["Mobile", "Desktop"], index=0) if mode == "🎮 Trainer" else "Mobile"

    if mode == "🔬 Range Lab":
        views.compare.show()
    elif mode == "📊 Stats":
        views.stats.show()
    else:
        if view == "Mobile":
            views.mobile.show()
        else:
            views.desktop.show()

if __name__ == "__main__":
    main()
