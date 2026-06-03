import streamlit as st
import pandas as pd
from util import read_data, calculate_budget, formated_budget, add_data, set_persen
# setting float
pd.options.display.float_format = '{:,.0f}'.format
st.title("Budget Saham Management")

tab1, tab2 = st.tabs(["Summary", "All"])
# Sidebar form for data entry
with st.sidebar:
    # option
    action = st.selectbox(
        "Choose an Action",
        [
            "Input New Stock",
            "Update Stock",
            "Delete Stock",
            "Setting %"
        ],
    )
    if action == "Input New Stock":
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
    elif action == "Update Stock":
        st.header("Update Stock")
        data = read_data()
        stock_to_update = st.selectbox("Select a Stock to Update", options=data["CodeStock"].tolist())
        stock_data = data[data["CodeStock"] == stock_to_update].iloc[0]
        with st.form(key="data_form"):
            buy_low = st.number_input(label="Buy Low*", min_value=0, step=1,value=int(stock_data["BuyLow"]))
            buy_high = st.number_input(label="Buy High*", min_value=0, step=1, value=int(stock_data["BuyHigh"]))
            total_budget = st.number_input(label="Total Budget*", min_value=0, step=1, value=int(stock_data["TotalBudget"]))
            update_submitted = st.form_submit_button("Submit")
            # Handle From Submisson
            if update_submitted:
                # Validate
                if buy_low <= 0 or buy_low <= 0 or total_budget <= 0 :
                    st.warning("Price or Budget dont 0")
                    st.stop()
                elif buy_low > buy_high:
                    st.warning("Buy High Must Bigger Thab Buy Low")
                    st.stop()
                else:
                     # Removing old entry
                    data.drop(data[data["CodeStock"] == stock_to_update].index,inplace=True)
                    # Create a new row of vendor data
                    input_data = pd.DataFrame(
                        [
                            {
                                "BuyLow": buy_low,
                                "BuyHigh" : buy_high,
                                "TotalBudget" : total_budget
                            }
                        ]
                    )
                    add_data(input_data,data)
                st.success("Update Stock successfully submitted!")
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
    ]].sort_values("CodeStock")

budget_display = formated_budget(data_display)
st.markdown(
    f"Estimation Budget : <span style='color:green'>Rp {budget_display}</span>",
    unsafe_allow_html=True
)

with tab1:
    data_summary = data_display[[
        "CodeStock",
        "EstimationBudget"
    ]].sort_values("CodeStock")
    st.dataframe(data_summary)

with tab2:
    st.dataframe(data_display)

