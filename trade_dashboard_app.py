
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load mock data
@st.cache_data
def load_data():
    return pd.read_csv("ProScalpTrader_Logs.csv", parse_dates=["Time"])

df = load_data()

st.title("📊 ProScalpTrader Dashboard")

# Filters
strategy = st.selectbox("Select Strategy", ["All"] + sorted(df["Strategy"].unique()))
symbol = st.selectbox("Select Symbol", ["All"] + sorted(df["Symbol"].unique()))

filtered = df.copy()
if strategy != "All":
    filtered = filtered[filtered["Strategy"] == strategy]
if symbol != "All":
    filtered = filtered[filtered["Symbol"] == symbol]

st.subheader("Trade Summary")
st.write(filtered[["Time", "Symbol", "Strategy", "Direction", "PnL", "Result"]].tail(10))

# Equity curve
st.subheader("📈 Equity Curve")
filtered["Cumulative PnL"] = filtered["PnL"].cumsum()
fig, ax = plt.subplots()
ax.plot(filtered["Time"], filtered["Cumulative PnL"], label="Equity Curve")
ax.set_xlabel("Time")
ax.set_ylabel("Cumulative PnL")
ax.legend()
st.pyplot(fig)

# Stats
st.subheader("📋 Summary Stats")
total_trades = len(filtered)
wins = (filtered["PnL"] > 0).sum()
losses = (filtered["PnL"] <= 0).sum()
win_rate = wins / total_trades * 100 if total_trades > 0 else 0
net_pnl = filtered["PnL"].sum()

st.metric("Total Trades", total_trades)
st.metric("Win Rate", f"{win_rate:.2f}%")
st.metric("Net PnL", f"${net_pnl:.2f}")
