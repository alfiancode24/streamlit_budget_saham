import streamlit as st
import pandas as pd
from util import read_data, calculate_budget, formated_budget, add_data
 
st.title("Budget Saham Management")

# Sidebar form for data entry
with st.sidebar:
    st.header("Enter New Stock")
    with st.form(key="data_form"):
        code_stock = st.text_input(label="Kode Saham").upper()
        buy_low = st.number_input(label="Buy Low*", min_value=0, value=0, step=1)
        buy_high = st.number_input(label="Buy High*", min_value=0, value=0, step=1)
        total_budget = st.number_input(label="Total Budget*", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Submit")
        # Handle From Submisson
        if submitted:
            # Validate
            if not code_stock:
                st.warning("Fill Code Stock")
                st.stop()
            elif buy_low <= 0 or buy_low <= 0 or total_budget <= 0 :
                st.warning("Price or Budget dont 0")
                st.stop()
            elif buy_low > buy_high:
                st.warning("Buy High Must Bigger Thab Buy Low")
                st.stop()
            else:
                # Create a new row of vendor data
                input_data = pd.DataFrame(
                    [
                        {
                            "CodeStock": code_stock+".JK",
                            "BuyLow": buy_low,
                            "BuyHigh" : buy_high,
                            "TotalBudget" : total_budget
                        }
                    ]
                )
                data = read_data()
                add_data(input_data,data)
            st.success("New Stock successfully submitted!")

# Display data
data = read_data()
data_display = calculate_budget(data)
data_display = data_display[[
        "CodeStock",
        "CurrentPrice",
        "TargetPrice",
        "BuyLow",
        "BuyHigh",
        "TotalBudget",
        "EstimationBudget"
    ]]

budget_display = formated_budget(data_display)
st.markdown(
    f"Estimation Budget : <span style='color:green'>Rp {budget_display}</span>",
    unsafe_allow_html=True
)
st.dataframe(data_display)