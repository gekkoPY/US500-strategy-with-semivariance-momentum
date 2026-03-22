---

### 3. READMESOURCE.md

```markdown
# Theoretical Framework: Asymmetric Realized Semivariance

This repository is built directly upon the quantitative mechanics outlined in advanced academic literature regarding market microstructure and momentum exhaustion.

## 📄 The Source Material
* **Paper Title:** *Time series momentum and reversal: Intraday information from realized semivariance*
* **Authors:** Liu, Lu, Li, Wang
* **Publication Year:** 2023

## 🧠 The Quantitative Thesis
Time-Series Momentum (TSM) algorithms classically suffer from violent, catastrophic reversals when institutional trends become behaviorally overextended. The authors theorized that the internal intraday volatility of an ongoing trend contains highly predictive mathematical information regarding its structural exhaustion. 

Instead of looking at overall daily volume or simple moving averages, this strategy decomposes standard variance into **asymmetric positive and negative realized semivariance**. 

The microstructure assumption is straightforward: 
* Sustainable, healthy trends exhibit balanced intraday retracements. 
* Exhausting, terminal trends exhibit parabolic, one-sided intraday volatility (the classic "blow-off top" or "panic sell").

## 🧮 The Mathematical Edge
The strategy continuously measures Realized Semivariance (RSV) using high-frequency 5-minute (M5) intraday returns, isolating upside volatility from downside volatility:

$$RSV_{t}^{+} = \sum_{i=1}^{n}r_{i,t}^{2}\mathbb{I}_{(r_{i,t}>0)}$$
$$RSV_{t}^{-} = \sum_{i=1}^{n}r_{i,t}^{2}\mathbb{I}_{(r_{i,t}<0)}$$

**How the Algorithm Uses This Data:**
The algorithmic strategy identifies imminent momentum reversals by aggregating these M5 intraday returns over a rolling 5-day window, and then comparing that figure against a long-term 250-day historical window. 

If the asset is currently engaged in a 20-day LONG momentum phase, but the positive realized semivariance ($RSV^+$) suddenly breaches the 80th percentile of the 250-day distribution, the system flags an institutional over-reaction.

Upon triggering this condition, the algorithm dynamically exits the momentum position, taking profit immediately before the inevitable reversal materializes. By using high-frequency intraday data purely for analytical purposes—and executing trades at a low, daily frequency—the system fiercely protects against transaction costs and retail spread friction.
