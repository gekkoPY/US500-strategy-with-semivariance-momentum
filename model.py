import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. STRATEGY PARAMETERS (US500)
# ==========================================
SYMBOL = "US500.pro" 
TIMEFRAME = mt5.TIMEFRAME_M5 
SPREAD = 0.8 # Standard US500 retail spread
MOMENTUM_LOOKBACK = 20 # 20-Day baseline momentum
PERCENTILE_THRESHOLD = 0.80 # 80th Percentile for exhaustion

print("\n" + "="*60)
print(f"📡 DOWNLOADING HISTORICAL DATA (2017-2021) FOR {SYMBOL}")
print("="*60)

if not mt5.initialize(): quit()

# HARDCODED HISTORICAL STRESS TEST DATES
start_date = datetime(2017, 1, 1)
end_date = datetime(2021, 12, 31)

rates = mt5.copy_rates_range(SYMBOL, TIMEFRAME, start_date, end_date)
mt5.shutdown()

if rates is None or len(rates) == 0:
    print(f"❌ MT5 returned no data! Scroll your M5 chart back to 2017 to cache history.")
    quit()

df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')
df.set_index('time', inplace=True)

print(f"✅ Loaded {len(df)} M5 Candles. Crunching Semivariance math...")

# ==========================================
# 2. HIGH-FREQUENCY SEMIVARIANCE ENGINE
# ==========================================
df['ret'] = df['close'].pct_change()
df['ret_sq'] = df['ret'] ** 2

df['rsv_pos'] = np.where(df['ret'] > 0, df['ret_sq'], 0)
df['rsv_neg'] = np.where(df['ret'] < 0, df['ret_sq'], 0)

daily_df = df.resample('D').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'rsv_pos': 'sum',
    'rsv_neg': 'sum'
}).dropna()

daily_df['rsv_pos_5d'] = daily_df['rsv_pos'].rolling(window=5).sum()
daily_df['rsv_neg_5d'] = daily_df['rsv_neg'].rolling(window=5).sum()

daily_df['rsv_pos_80th'] = daily_df['rsv_pos_5d'].rolling(window=250).quantile(PERCENTILE_THRESHOLD)
daily_df['rsv_neg_80th'] = daily_df['rsv_neg_5d'].rolling(window=250).quantile(PERCENTILE_THRESHOLD)

daily_df['mom_20d'] = daily_df['close'].pct_change(periods=MOMENTUM_LOOKBACK)

daily_df.dropna(inplace=True) 

# ==========================================
# 3. DAILY REBALANCING EXECUTION
# ==========================================
print("⚙️ Simulating Daily Portfolio Rebalancing (2018-2021)...")

equity = 0.0
equity_curve = [0.0]
current_position = 0 
entry_price = 0.0
results = []
days_in_cash = 0

for date, row in daily_df.iterrows():
    target_position = 0
    
    if row['mom_20d'] > 0 and row['rsv_pos_5d'] < row['rsv_pos_80th']:
        target_position = 1
    elif row['mom_20d'] < 0 and row['rsv_neg_5d'] < row['rsv_neg_80th']:
        target_position = -1
    else:
        target_position = 0
        days_in_cash += 1

    next_day_open = row['open'] 
    
    if target_position != current_position:
        if current_position == 1:
            pnl = (next_day_open - SPREAD) - entry_price
            equity += pnl
            results.append(pnl)
        elif current_position == -1:
            pnl = entry_price - (next_day_open + SPREAD)
            equity += pnl
            results.append(pnl)
            
        current_position = target_position
        if current_position == 1:
            entry_price = next_day_open + SPREAD
        elif current_position == -1:
            entry_price = next_day_open - SPREAD
            
    mark_pnl = 0
    if current_position == 1: mark_pnl = row['close'] - entry_price
    elif current_position == -1: mark_pnl = entry_price - row['close']
    equity_curve.append(equity + mark_pnl)

# ==========================================
# 4. STATS, DRAWDOWN & VISUALIZATION
# ==========================================
total_trades = len(results)
win_rate = len([r for r in results if r > 0]) / total_trades * 100 if total_trades > 0 else 0

running_max = np.maximum.accumulate(equity_curve)
drawdowns = running_max - equity_curve
max_drawdown = np.max(drawdowns) if len(drawdowns) > 0 else 0

print("\n" + "="*60)
print("🏆 HISTORICAL STRESS TEST: RSV MOMENTUM (2018-2021)")
print("="*60)
print(f"➤ Total Trades Taken : {total_trades}")
print(f"➤ Days Spent in Cash : {days_in_cash} (Avoiding crashes)")
print(f"➤ Win Rate           : {win_rate:.2f}%")
print(f"➤ Maximum Drawdown   : -{max_drawdown:.2f} Points")
print(f"➤ Final Net Profit   : {equity:.2f} Points")
print("="*60)

fig = go.Figure(go.Scatter(y=equity_curve, mode='lines', fill='tozeroy', line=dict(color='#FF00FF')))
fig.update_layout(title="Historical Stress Test: RSV Momentum (US500, 2018-2021)", template="plotly_dark")
fig.write_html("us500_historical_stress.html", auto_open=True)
print("✅ Backtest Complete. Check your browser.")
