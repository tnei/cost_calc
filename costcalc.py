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

# Create tabs for separate calculators
tab1, tab2, tab3, tab4 = st.tabs(["Snowflake Calculator", "Fivetran Calculator", "Rivery Calculator", "Airbyte Calculator"])

# Snowflake Calculator
with tab1:
    st.title("Snowflake Cost Calculator")
    st.subheader("Calculate costs for Snowflake usage based on detailed parameters")

    # Input Parameters
    service_edition = st.selectbox("Service Edition", service_editions)
    warehouse_size = st.selectbox("Warehouse Size", list(warehouse_sizes.keys()))
    region = st.selectbox("Cloud Provider and Region", list(cloud_regions.keys()))
    weekday_uptime = st.number_input("DW Uptime on Weekdays (hrs)", min_value=0, step=1)
    weekend_uptime = st.number_input("DW Uptime on Weekends (hrs)", min_value=0, step=1)
    storage_tb = st.number_input("Storage (TB)", min_value=0.0, step=0.1)

    # Calculations
    credits_per_hour = warehouse_sizes[warehouse_size]
    cost_per_credit = cloud_regions[region]
    total_uptime_hours = (weekday_uptime * 5) + (weekend_uptime * 2)  # Uptime per week
    total_credits = credits_per_hour * total_uptime_hours
    dw_cost = total_credits * cost_per_credit
    storage_cost_per_tb = storage_costs[service_edition]
    storage_cost = storage_tb * storage_cost_per_tb
    total_cost = dw_cost + storage_cost

    # Output Results
    st.header("Cost Breakdown")
    st.write(f"**Service Edition:** {service_edition}")
    st.write(f"**Warehouse Size:** {warehouse_size}")
    st.write(f"**Region:** {region}")
    st.write(f"**Total Uptime Hours per Week:** {total_uptime_hours}")
    st.write(f"**Total Credits Consumed:** {total_credits}")
    st.write(f"**DW Cost:** ${dw_cost:,.2f}")
    st.write(f"**Storage Cost:** ${storage_cost:,.2f}")
    st.write(f"**Total Cost:** ${total_cost:,.2f}")

# Fivetran Calculator
with tab2:
    st.title("Fivetran Cost Calculator")
    st.subheader("Calculate Fivetran costs based on MAR and tier")

    # User Inputs
    monthly_active_rows = st.number_input("Monthly Active Rows (in Millions)", min_value=0.0, step=1.0)
    projected_growth = st.number_input("Projected Annual Growth (%)", min_value=0, step=1)
    fivetran_tier = st.selectbox("Fivetran Tier", list(fivetran_tiers.keys()))

    # Calculations
    tier = fivetran_tiers[fivetran_tier]
    base_cost = tier["base_cost"]
    cost_per_mar = tier["cost_per_mar"]
    total_mar = monthly_active_rows + (monthly_active_rows * projected_growth / 100)
    additional_cost = max(0, (total_mar - 10) * cost_per_mar)
    total_monthly_cost = base_cost + additional_cost
    total_annual_cost = total_monthly_cost * 12

    # Output Results
    st.header("Cost Breakdown")
    st.write(f"**Fivetran Tier:** {fivetran_tier}")
    st.write(f"**Total MAR (with Growth):** {total_mar:,.2f}M")
    st.write(f"**Total Monthly Cost:** ${total_monthly_cost:,.2f}")
    st.write(f"**Total Annual Cost:** ${total_annual_cost:,.2f}")

# Rivery Calculator
with tab3:
    st.title("Rivery Cost Calculator")
    st.subheader("Estimate costs for Rivery platform usage")

    # Inputs for Rivery
    base_cost = 2083
    extra_rpu = st.number_input("Additional RPU Credits Used", min_value=0, step=1)
    cost_per_rpu = 0.1  # Example cost per RPU
    additional_cost = extra_rpu * cost_per_rpu
    total_cost = base_cost + additional_cost

    # Output Results
    st.header("Cost Breakdown")
    st.write(f"**Base Cost:** ${base_cost}")
    st.write(f"**Additional RPU Credits Used:** {extra_rpu}")
    st.write(f"**Additional Cost:** ${additional_cost:.2f}")
    st.write(f"**Total Cost:** ${total_cost:.2f}")

# Airbyte Calculator
with tab4:
    st.title("Airbyte Cost Calculator")
    st.subheader("Estimate costs for Airbyte platform usage")

    # Inputs for Airbyte
    rows_processed = st.number_input("Monthly Rows Processed (in Millions)", min_value=0, step=1)
    data_volume = st.number_input("Monthly Data Volume (in GB)", min_value=0, step=1)
    row_cost = 6 * 2.5 / 1000  # Cost per row
    volume_cost = 4 * 2.5 / 1000  # Cost per GB
    total_row_cost = rows_processed * row_cost
    total_volume_cost = data_volume * volume_cost
    total_cost = total_row_cost + total_volume_cost

    # Output Results
    st.header("Cost Breakdown")
    st.write(f"**Total Rows Processed:** {rows_processed}M")
    st.write(f"**Total Data Volume:** {data_volume} GB")
    st.write(f"**Cost for Rows Processed:** ${total_row_cost:.2f}")
    st.write(f"**Cost for Data Volume:** ${total_volume_cost:.2f}")
    st.write(f"**Total Cost:** ${total_cost:.2f}")
