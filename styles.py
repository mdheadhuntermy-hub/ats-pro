import streamlit as st


def cargar_estilos():

    st.markdown('''
    <style>

    .main {
        background-color:#0f172a;
    }

    h1,h2,h3,h4 {
        color:white !important;
    }

    p,label,div {
        color:#e2e8f0;
    }

    .stButton > button {
        background:linear-gradient(90deg,#2563eb,#3b82f6);
        color:white;
        border:none;
        border-radius:12px;
        width:100%;
    }

    footer {
        visibility:hidden;
    }

    #MainMenu {
        visibility:hidden;
    }

    </style>
    ''', unsafe_allow_html=True)