import os
import yfinance as yf
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_data(tickers, start_date, end_date):
    data_dict = {}
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start_date,
                             end=end_date, progress=False)
            if not df.empty:
                data_dict[ticker] = df
                logging.info(f"Data fetched for {ticker}")
            else:
                logging.warning(f"No data found for {ticker}")
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
    return data_dict


def save_data(data_dict, output_dir="data"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for ticker, df in data_dict.items():
        csv_path = os.path.join(output_dir, f"{ticker}.csv")
        df.to_csv(csv_path)
        logging.info(f"Data saved for {ticker} at {csv_path}")


if __name__ == "__main__":
    tickers = ["AAPL", "TSLA", "GOOGL"]
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    stock_data = fetch_data(tickers, start_date, end_date)
    save_data(stock_data, output_dir="data")
    logging.info("Data fetch complete.")
