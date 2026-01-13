import streamlit as st

def apply_global_style():
    st.markdown(
        """
        <style>
          .title-big { font-size: 1.7rem; font-weight: 800; }
          .subtle { color: rgba(255,255,255,0.7); }
          .pill {
            display:inline-block; padding: 0.35rem 0.6rem; border-radius: 999px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            font-size: 0.85rem;
          }
          .section-title { font-size: 1.05rem; font-weight: 700; margin: 0.2rem 0 0.2rem 0; }
        </style>
        """,
        unsafe_allow_html=True
    )
