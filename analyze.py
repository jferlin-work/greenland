import os
import pandas as pd
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_data(ticker, data_dir="data"):
    csv_path = os.path.join(data_dir, f"{ticker}.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
        logging.info(f"Data loaded for {ticker}")
        return df
    else:
        logging.warning(f"No data found for {ticker}")
        return pd.DataFrame()  # empty df if not found


def simple_moving_average_signal(df, short_window=20, long_window=50):
    df["SMA_short"] = df["Close"].rolling(window=short_window).mean()
    df["SMA_long"] = df["Close"].rolling(window=long_window).mean()

    latest_short = df["SMA_short"].iloc[-1]
    latest_long = df["SMA_long"].iloc[-1]

    if np.isnan(latest_short) or np.isnan(latest_long):
        return "NO SIGNAL"
    elif latest_short > latest_long:
        return "BUY"
    elif latest_short < latest_long:
        return "SELL"
    else:
        return "HOLD"


def generate_recommendations(tickers, short_window=20, long_window=50):
    recommendations = {}
    for ticker in tickers:
        df = load_data(ticker)
        if df.empty:
            recommendations[ticker] = "NO DATA"
            continue

        signal = simple_moving_average_signal(df, short_window, long_window)
        recommendations[ticker] = signal
    return recommendations


if __name__ == "__main__":
    tickers = ["AAPL", "TSLA", "GOOGL"]
    results = generate_recommendations(tickers)

    logging.info("=== RECOMMENDATIONS ===")
    for ticker, rec in results.items():
        logging.info(f"{ticker}: {rec}")
