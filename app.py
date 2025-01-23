# pylint: disable=missing-module-docstring
import io
import ast
import duckdb
import pandas as pd
import streamlit as st

# Connexion à la base de données DuckDB
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    exercice = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df().sort_values("last_reviewed").reset_index()
    st.write(exercice)

    exercise_name = exercice.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(f"result has a {n_lines_difference} lines difference with the solution_df")

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    # Extraction et affichage des tables en fonction de la base de données
    exercice_tables = exercice.loc[0, "tables"]
    for table in exercice_tables:
        st.write(f"tables: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)
