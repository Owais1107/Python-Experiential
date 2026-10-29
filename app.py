import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Smart Home Energy Monitor",
    page_icon="⚡",
    layout="wide",
)

st.markdown("""
<style>
    .main {background-color: #f7f9fc;}
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    div[data-testid="stMetric"] {
        background: white; padding: 16px 18px; border-radius: 12px;
        border: 1px solid #e6eaf0; box-shadow: 0 2px 8px rgba(20,30,50,.04);
    }
    .hero {
        padding: 24px; border-radius: 16px; color: white;
        background: linear-gradient(120deg, #123b5d, #147d72);
        margin-bottom: 20px;
    }
    .hero h1 {margin: 0 0 8px 0; font-size: 2.1rem;}
    .hero p {margin: 0; opacity: .92;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>⚡ Smart Home Energy Consumption Monitor</h1>
  <p>Track appliance-wise electricity usage, estimate your bill, identify energy-hungry devices, and find practical ways to save.</p>
</div>
""", unsafe_allow_html=True)

DEFAULT_APPLIANCES = pd.DataFrame([
    {"Appliance": "Air Conditioner", "Power (W)": 1500, "Hours per day": 6.0, "Quantity": 1},
    {"Appliance": "Refrigerator", "Power (W)": 180, "Hours per day": 8.0, "Quantity": 1},
    {"Appliance": "Television", "Power (W)": 100, "Hours per day": 4.0, "Quantity": 1},
    {"Appliance": "Ceiling Fan", "Power (W)": 75, "Hours per day": 10.0, "Quantity": 3},
    {"Appliance": "LED Lights", "Power (W)": 12, "Hours per day": 6.0, "Quantity": 6},
    {"Appliance": "Washing Machine", "Power (W)": 500, "Hours per day": 0.7, "Quantity": 1},
])

if "appliances" not in st.session_state:
    st.session_state.appliances = DEFAULT_APPLIANCES.copy()

with st.sidebar:
    st.header("⚙️ Settings")
    days = st.number_input("Days in billing period", min_value=1, max_value=366, value=30, step=1)
    tariff = st.number_input("Electricity rate (₹ per kWh)", min_value=0.0, value=8.0, step=0.5)
    high_usage_threshold = st.number_input(
        "Flag appliances above (kWh per billing period)",
        min_value=0.0, value=50.0, step=5.0
    )
    st.caption("Estimates are based on the power and usage values you enter. Actual bills may vary.")

st.subheader("1. Appliance usage")
st.write("Edit the sample values or add your own appliances. Power is measured in watts (W).")

edited = st.data_editor(
    st.session_state.appliances,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "Appliance": st.column_config.TextColumn("Appliance", required=True),
        "Power (W)": st.column_config.NumberColumn("Power (W)", min_value=0, step=10, format="%d"),
        "Hours per day": st.column_config.NumberColumn("Hours per day", min_value=0.0, max_value=24.0, step=0.5, format="%.1f"),
        "Quantity": st.column_config.NumberColumn("Quantity", min_value=1, step=1, format="%d"),
    },
    key="appliance_editor",
)
st.session_state.appliances = edited.copy()

df = edited.copy()
if df.empty:
    st.info("Add at least one appliance in the table to see your report.")
    st.stop()

for col in ["Power (W)", "Hours per day", "Quantity"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["Appliance"] = df["Appliance"].fillna("").astype(str).str.strip()
df = df[(df["Appliance"] != "") & (df["Power (W)"] >= 0) & (df["Hours per day"] >= 0) & (df["Quantity"] >= 0)].copy()
df["Daily Energy (kWh)"] = df["Power (W)"] * df["Hours per day"] * df["Quantity"] / 1000
df["Period Energy (kWh)"] = df["Daily Energy (kWh)"] * days
df["Estimated Cost (₹)"] = df["Period Energy (kWh)"] * tariff
df["Daily Cost (₹)"] = df["Daily Energy (kWh)"] * tariff

if df.empty:
    st.warning("Please enter at least one appliance with a name.")
    st.stop()

total_energy = df["Period Energy (kWh)"].sum()
total_cost = df["Estimated Cost (₹)"].sum()
daily_energy = df["Daily Energy (kWh)"].sum()
high_appliances = df[df["Period Energy (kWh)"] >= high_usage_threshold]
top = df.sort_values("Period Energy (kWh)", ascending=False).iloc[0]

st.subheader("2. Energy overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total energy", f"{total_energy:,.1f} kWh", f"{daily_energy:,.2f} kWh/day")
m2.metric("Estimated bill", f"₹{total_cost:,.0f}", f"₹{total_cost / days:,.2f}/day")
m3.metric("Appliances tracked", f"{len(df)}")
m4.metric("High-usage devices", f"{len(high_appliances)}")

left, right = st.columns(2)
with left:
    st.markdown("#### Energy use by appliance")
    energy_fig = px.bar(
        df.sort_values("Period Energy (kWh)", ascending=True),
        x="Period Energy (kWh)", y="Appliance", orientation="h",
        color="Period Energy (kWh)", color_continuous_scale="Teal",
        labels={"Period Energy (kWh)": "Energy (kWh)", "Appliance": ""},
    )
    energy_fig.update_layout(coloraxis_showscale=False, margin=dict(l=10, r=10, t=15, b=10))
    st.plotly_chart(energy_fig, use_container_width=True)

with right:
    st.markdown("#### Share of total consumption")
    pie_fig = px.pie(
        df, names="Appliance", values="Period Energy (kWh)", hole=0.48,
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    pie_fig.update_traces(textposition="inside", textinfo="percent+label")
    pie_fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=15, b=10))
    st.plotly_chart(pie_fig, use_container_width=True)

st.subheader("3. Appliance-wise report")
report = df[[
    "Appliance", "Power (W)", "Hours per day", "Quantity",
    "Daily Energy (kWh)", "Period Energy (kWh)", "Estimated Cost (₹)"
]].sort_values("Period Energy (kWh)", ascending=False)
st.dataframe(
    report.style.format({
        "Power (W)": "{:,.0f}",
        "Hours per day": "{:.1f}",
        "Quantity": "{:,.0f}",
        "Daily Energy (kWh)": "{:.2f}",
        "Period Energy (kWh)": "{:.2f}",
        "Estimated Cost (₹)": "₹{:,.2f}",
    }),
    use_container_width=True,
    hide_index=True,
)

csv = report.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download appliance report (CSV)",
    data=csv,
    file_name="smart_home_energy_report.csv",
    mime="text/csv",
)

st.subheader("4. Energy-saving recommendations")
recommendations = []
for _, row in df.iterrows():
    name = row["Appliance"]
    lower = name.lower()
    kwh = row["Period Energy (kWh)"]
    hours = row["Hours per day"]
    cost = row["Estimated Cost (₹)"]

    if any(word in lower for word in ["air conditioner", "ac", "heater", "geyser", "water heater"]):
        recommendations.append((name, "High-power appliance", "Try a 1–2°C more efficient thermostat setting, use timers, and clean filters regularly."))
    elif any(word in lower for word in ["light", "bulb", "lamp"]):
        recommendations.append((name, "Lighting", "Switch off unused lights and use LED bulbs wherever possible."))
    elif any(word in lower for word in ["refrigerator", "fridge"]):
        recommendations.append((name, "Cooling", "Keep the door closed, allow ventilation around the unit, and set the temperature appropriately."))
    elif any(word in lower for word in ["washing", "washer", "dryer"]):
        recommendations.append((name, "Laundry", "Run full loads and use cold-water or eco modes when suitable."))
    elif any(word in lower for word in ["tv", "television", "computer", "desktop", "gaming", "console"]):
        recommendations.append((name, "Standby power", "Enable power-saving mode and switch off at the plug when not in use for long periods."))
    elif hours >= 8:
        recommendations.append((name, "Long operating time", "Review whether operating hours can be reduced or use an efficient model."))
    elif kwh >= high_usage_threshold:
        recommendations.append((name, "High consumption", "Check the usage schedule and compare the device's energy rating with efficient alternatives."))

if len(high_appliances):
    st.warning(
        "High-energy devices: " + ", ".join(high_appliances["Appliance"].tolist())
        + ". Review these first because they meet or exceed your selected threshold."
    )
else:
    st.success("No appliance meets your current high-usage threshold.")

if recommendations:
    for name, category, tip in recommendations:
        st.markdown(f"**{name} — {category}:** {tip}")
else:
    st.info("No specific recommendation was triggered. Try reviewing the highest-consuming appliances in the chart.")

# Illustrative savings scenario: reduce usage of the highest-consuming appliance by 10%.
potential_saving_kwh = top["Period Energy (kWh)"] * 0.10
potential_saving_rupees = potential_saving_kwh * tariff
st.markdown("#### 💡 Example saving opportunity")
st.write(
    f"If you reduce the usage of **{top['Appliance']}** by 10%, you could save approximately "
    f"**{potential_saving_kwh:.1f} kWh** and **₹{potential_saving_rupees:,.0f}** over {days} days, "
    "assuming the same electricity rate."
)

with st.expander("How are the calculations made?"):
    st.latex(r"\\text{Daily energy (kWh)} = \\frac{\\text{Power (W)} \\times \\text{Hours/day} \\times \\text{Quantity}}{1000}")
    st.latex(r"\\text{Period energy (kWh)} = \\text{Daily energy} \\times \\text{Billing days}")
    st.latex(r"\\text{Estimated cost} = \\text{Period energy (kWh)} \\times \\text{Rate per kWh}")
    st.caption("This is an educational estimation tool, not a replacement for your electricity provider's meter or bill.")

st.markdown("---")
st.caption("Smart Home Energy Consumption Monitor • Built with Python and Streamlit")
