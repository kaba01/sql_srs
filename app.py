# pylint: disable=missing-module-docstring
import io
import os
import logging

import ast
import duckdb
import pandas as pd
import streamlit as st
from datetime import date, timedelta, datetime

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run(["python", "init_db.py"])

# Connexion à la base de données DuckDB
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

def check_users_solution(user_query: str) -> None:
    '''
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    '''

    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct !")
            st.balloons()
    except KeyError:
        st.write("Some columns are missing")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(f"result has a {n_lines_difference} lines difference with the solution_df")


with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )

    if theme:
        st.write(f"You selected {theme}")
        select_exercises_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercises_query = f"SELECT * FROM memory_state"

        exercice = (
            con.execute(select_exercises_query)
            .df()
            .sort_values("last_reviewed")
            .reset_index(drop=True)
        )

    st.write(exercice)
    exercise_name = exercice.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="user_input")


if query:
    check_users_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f"revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'")
        st.rerun()

if st.button("Reset"):
    con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()




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
