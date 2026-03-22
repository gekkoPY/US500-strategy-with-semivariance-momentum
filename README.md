# US500 RSV Momentum Overlay

An advanced quantitative trading algorithm designed to trade the S&P 500 (US500) using Time-Series Momentum, heavily filtered by high-frequency intraday volatility metrics to predict and avoid market crashes.

## 📌 Overview
Standard trend-following strategies are historically robust, but they suffer from catastrophic drawdowns during "momentum crashes" (e.g., the 2018 Volmageddon, the 2020 COVID-19 Flash Crash). 

This algorithm solves that structural flaw. It operates on the hypothesis that the internal, high-frequency volatility of an ongoing trend contains mathematical proof of its exhaustion. By decomposing standard M5 (5-minute) variance into asymmetric upside and downside semivariance, the bot accurately detects retail "blow-off tops" and institutional panic, stepping aside into cash *before* the crash materializes.

## ⚙️ Core Mechanics
* **Target Asset:** US500 (S&P 500 CFDs / SPY)
* **Analytical Timeframe:** High-Frequency M5 (5-minute) Returns
* **Execution Timeframe:** Daily Rebalancing (Low Frequency)
* **The Filter:** 250-Day Rolling 80th Percentile of Realized Semivariance (RSV)

## 📊 Backtest Performance (2018 - 2021 Stress Test)
Tested against the most volatile market regimes of the last decade, the algorithm demonstrated exceptional capital preservation by spending **217 days in cash** during structural market collapses.

* **Win Rate:** 65.52%
* **Maximum Historical Drawdown:** ~11.4% (Based on $2,500 baseline margin)
* **Net Return on Equity (ROE):** ~144%

## 🚀 Installation & Usage
1. Ensure you have [MetaTrader 5](https://www.metatrader5.com/) installed and logged into a broker providing `US500` data (e.g., OANDA).
2. Install the required Python libraries:
   ```bash
   pip install MetaTrader5 pandas numpy plotly

  
