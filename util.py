import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from streamlit_gsheets import GSheetsConnection

def read_data():
    # Connect to the Google Sheet
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Connect Sheet
    sheet = conn.read(worksheet="budget_saham", usecols=list(range(6)), ttl=5)
    sheet = sheet.dropna(how="all")
    return sheet

def get_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.fast_info["lastPrice"]
        return price
    except:
        return None

def calculate_budget(data):
    # price stock
    data["CurrentPrice"] = data["CodeStock"].apply(get_price)
    
    # target price
    data["TargetPrice"] = data["CurrentPrice"] * 0.97

    # Condition
    condition = (
        (data["CurrentPrice"] >= data["BuyLow"]) & (data["TargetPrice"] <= data["BuyHigh"])
    )
    # Estimation Budget
    data ["EstimationBudget"] = np.minimum(
        data ["TotalBudget"],
        np.where(
            condition,
            (data["BuyHigh"] - data["TargetPrice"]) *
            (data["TotalBudget"] / (data["BuyHigh"] - data["BuyLow"])),
            0
        )
    ).astype(int)
    return data

def formated_budget(data):
    total = data["EstimationBudget"].sum()
    total = f"{total:,.0f}".replace(",", ".")
    return total

def add_data(input_data,data):
    conn = st.connection("gsheets", type=GSheetsConnection)
    # add input data to dataframe
    update_data = pd.concat([data,input_data], ignore_index=True)

    # Update to Gsheet
    conn.update(worksheet="budget_saham", data=update_data)