import streamlit as st

# App Title
st.title("Data Integration Platform Cost Calculator")
st.subheader("Compare Costs for Fivetran, Rivery, and Airbyte")

# User Inputs
st.sidebar.header("Input Parameters")
initial_data_load = st.sidebar.number_input("Initial Data Load (GB)", min_value=0.0, step=1.0)
daily_incremental_data = st.sidebar.number_input("Daily Incremental Data (MB)", min_value=0.0, step=1.0)
monthly_active_rows = st.sidebar.number_input("Monthly Active Rows (in Millions)", min_value=0.0, step=1.0)
projected_growth = st.sidebar.number_input("Projected Annual Growth (%)", min_value=0, step=1)
platform = st.sidebar.selectbox("Platform", ["Fivetran", "Rivery", "Airbyte"])
fivetran_tier = st.sidebar.selectbox("Fivetran Tier", ["Enterprise", "Business Critical"], disabled=(platform != "Fivetran"))

# Calculations
if platform == "Fivetran":
    base_cost = 4000 if fivetran_tier == "Enterprise" else 10000
    cost_per_mar = 94.44 if fivetran_tier == "Enterprise" else 55.56
    total_mar = monthly_active_rows + (monthly_active_rows * projected_growth / 100)
    additional_cost = max(0, (total_mar - 10) * cost_per_mar)
    monthly_cost = base_cost + additional_cost
    initial_setup = "Included in Monthly Cost"
elif platform == "Rivery":
    monthly_cost = 2083
    initial_setup = "Free Initial Load of 4TB"
elif platform == "Airbyte":
    api_credits_cost = daily_incremental_data * 30 * 6 * 2.5 / 1000
    db_credits_cost = monthly_active_rows * 4 * 2.5
    monthly_cost = api_credits_cost + db_credits_cost
    initial_setup = f"{initial_data_load * 4 * 2.5} USD"
else:
    monthly_cost = 0
    initial_setup = "N/A"

annual_cost = monthly_cost * 12

# Output Results
st.header("Cost Breakdown")
st.write(f"**Platform:** {platform}")
if platform == "Fivetran":
    st.write(f"**Fivetran Tier:** {fivetran_tier}")
st.write(f"**Monthly Cost:** ${monthly_cost:,.2f}")
st.write(f"**Annual Cost:** ${annual_cost:,.2f}")
st.write(f"**Initial Setup Cost:** {initial_setup}")

# Display Disclaimer
st.markdown("""
---
*This calculator provides estimated costs based on inputs and platform pricing details.*
""")
