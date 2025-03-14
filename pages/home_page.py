import streamlit as st
import pandas as pd
from db_setup import Session
from sqlalchemy import text

def display():
    st.header("Search and Filter Contractors")
    session = Session()

    with st.expander("Search and Filter Options", expanded=True):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            search_query = st.text_input("Search by keyword", key="search_keyword")
        with col2:
            selected_service = st.selectbox("Filter by service", ["All"] + get_services(), key="filter_service")
        with col3:
            selected_city = st.text_input("Filter by city", key="filter_city")

    query = "SELECT * FROM contractors WHERE 1=1"
    params = {}

    if search_query:
        query += " AND (name LIKE :search_query OR number LIKE :search_query OR city LIKE :search_query OR service LIKE :search_query OR feedback LIKE :search_query)"
        params["search_query"] = f"%{search_query}%"
    if selected_service != "All":
        query += " AND service = :selected_service"
        params["selected_service"] = selected_service
    if selected_city:
        query += " AND city LIKE :selected_city"
        params["selected_city"] = f"%{selected_city}%"

    result = session.execute(text(query), params)
    rows = result.fetchall()
    columns = result.keys()
    df = pd.DataFrame([dict(zip(columns, row)) for row in rows])

    st.data_editor(
        df,
        column_config={
            "name": st.column_config.TextColumn("Name"),
            "number": st.column_config.TextColumn("Number"),
            "city": st.column_config.TextColumn("City"),
            "service": st.column_config.TextColumn("Service"),
            "feedback": st.column_config.TextColumn("Feedback"),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        disabled=True,  # This will make the table read-only
        key="contractor_table"
    )

    session.close()

def get_services():
    session = Session()
    result = session.execute(text("SELECT service_name FROM services"))
    services = [row[0] for row in result.fetchall()]  # Changed this line
    session.close()
    if not services:
        services = ["Plumbing", "Tiles", "False Ceiling", "Mesh Door", "Painting", "Electrical Work", "Carpentry", "Flooring", "Masonry", "HVAC", "Landscaping", "Cleaning", "Pest Control"]
    return services