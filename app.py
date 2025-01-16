import streamlit as st
import pandas as pd
import duckdb

st.cache_data.clear()

st.write("""
# SQL SRS
Spaced Repetition System SQL practice 
""")

option = st.selectbox(
    "What would you like to review ?",
    ("Joins", "GroupBy", "Windows Functions"),
    index=None,
    placeholder="Select a theme..."
)

st.write("You selected:", option)


data = {"a": [1, 2, 3], "b": [5, 6, 7]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    sql_query = st.text_area(label="Entrez votre input")
    result = duckdb.query(sql_query)
    st.write(f"la requête suivante: {sql_query}")
    st.dataframe(result)


with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

