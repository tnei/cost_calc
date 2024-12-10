import streamlit as st

# Data for Snowflake pricing
service_editions = ["Standard", "Enterprise", "Business Critical", "Virtual Private Snowflake"]
warehouse_sizes = {
    "XS": 1,
    "S": 2,
    "M": 4,
    "M Snowpark Optimized": 6,
    "L": 8,
    "L Snowpark Optimized": 12,
    "XL": 16,
    "XL Snowpark Optimized": 24,
    "2XL": 32,
    "2XL Snowpark Optimized": 48,
    "3XL": 64,
    "3XL Snowpark Optimized": 96,
    "4XL": 128,
    "4XL Snowpark Optimized": 192,
    "5XL": 256,
    "5XL Snowpark Optimized": 384,
    "6XL": 512,
    "6XL Snowpark Optimized": 768
}
cloud_regions = {
    "AWS US East (Northern Virginia)": 2,
    "AWS EU Dublin": 2.6,
    "Azure East US 2 (Virginia)": 2,
    "Azure West Europe (Netherlands)": 2.6,
    "GCP US Central 1 (Iowa)": 2,
    "GCP Europe West 4 (Netherlands)": 2.6
}
storage_costs = {
    "Standard": 23,  # Example: 23 USD/TB
    "Enterprise": 25,
    "Business Critical": 30,
    "Virtual Private Snowflake": 40
}

# Data for Fivetran pricing
fivetran_tiers = {
    "Starter": {"base_cost": 2000, "cost_per_mar": 47.22},
    "Standard": {"base_cost": 3000, "cost_per_mar": 70.83},
    "Enterprise": {"base_cost": 4000, "cost_per_mar": 94.44},
    "Business Critical": {"base_cost": 10000, "cost_per_mar": 55.56},
}

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Snowflake Calculator", "Fivetran Calculator"])

if page == "Snowflake Calculator":
    # Snowflake Calculator
    st.title("Snowflake Cost Calculator")
    st.subheader("Calculate costs for Snowflake usage based on detailed parameters")

    # Input Parameters
    st.sidebar.header("Input Parameters")
    service_edition = st.sidebar.selectbox("Service Edition", service_editions)
    warehouse_size = st.sidebar.selectbox("Warehouse Size", list(warehouse_sizes.keys()))
    region = st.sidebar.selectbox("Cloud Provider and Region", list(cloud_regions.keys()))
    weekday_uptime = st.sidebar.number_input("DW Uptime on Weekdays (hrs)", min_value=0, step=1)
    weekend_uptime = st.sidebar.number_input("DW Uptime on Weekends (hrs)", min_value=0, step=1)
    storage_tb = st.sidebar.number_input("Storage (TB)", min_value=0.0, step=0.1)

    # Calculations
    # Calculate DW costs
    credits_per_hour = warehouse_sizes[warehouse_size]
    cost_per_credit = cloud_regions[region]
    total_uptime_hours = (weekday_uptime * 5) + (weekend_uptime * 2)  # Uptime per week
    total_credits = credits_per_hour * total_uptime_hours
    dw_cost = total_credits * cost_per_credit

    # Calculate storage costs
    storage_cost_per_tb = storage_costs[service_edition]
    storage_cost = storage_tb * storage_cost_per_tb

    # Total cost
    total_cost = dw_cost + storage_cost

    # Output Results
    st.header("Cost Breakdown")
    st.write(f"**Service Edition:** {service_edition}")
    st.write(f"**Warehouse Size:** {warehouse_size}")
    st.write(f"**Region:** {region}")
    st.write(f"**DW Uptime on Weekdays:** {weekday_uptime} hrs")
    st.write(f"**DW Uptime on Weekends:** {weekend_uptime} hrs")
    st.write(f"**Total Uptime Hours per Week:** {total_uptime_hours}")
    st.write(f"**Total Credits Consumed:** {total_credits}")
    st.write(f"**DW Cost:** ${dw_cost:,.2f}")
    st.write(f"**Storage Cost:** ${storage_cost:,.2f}")
    st.write(f"**Total Cost:** ${total_cost:,.2f}")

elif page == "Fivetran Calculator":
    # Fivetran Calculator
    st.title("Fivetran Cost Calculator")
    st.subheader("Calculate Fivetran costs based on MAR and tier")

    # User Inputs
    st.sidebar.header("Input Parameters")
    monthly_active_rows = st.sidebar.number_input("Monthly Active Rows (in Millions)", min_value=0.0, step=1.0)
    projected_growth = st.sidebar.number_input("Projected Annual Growth (%)", min_value=0, step=1)
    fivetran_tier = st.sidebar.selectbox("Fivetran Tier", list(fivetran_tiers.keys()))

    # Calculations
    tier = fivetran_tiers[fivetran_tier]
    base_cost = tier["base_cost"]
    cost_per_mar = tier["cost_per_mar"]

    # Calculate MAR including growth
    total_mar = monthly_active_rows + (monthly_active_rows * projected_growth / 100)

    # Calculate additional costs
    additional_cost = max(0, (total_mar - 10) * cost_per_mar)
    total_monthly_cost = base_cost + additional_cost
    total_annual_cost = total_monthly_cost * 12

    # Output Results
    st.header("Cost Breakdown")
    st.write(f"**Fivetran Tier:** {fivetran_tier}")
    st.write(f"**Base Cost:** ${base_cost:,.2f}")
    st.write(f"**Total MAR (with Growth):** {total_mar:,.2f}M")
    st.write(f"**Additional Cost:** ${additional_cost:,.2f}")
    st.write(f"**Total Monthly Cost:** ${total_monthly_cost:,.2f}")
    st.write(f"**Total Annual Cost:** ${total_annual_cost:,.2f}")

# Disclaimer
st.markdown("""
---
*This calculator provides estimated costs based on pricing details as of February 2024.*
""")
