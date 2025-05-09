import pandas as pd
from datetime import datetime
from ..common import common


def _from_withdrawals_df(df: pd.DataFrame) -> pd.DataFrame:
  df = df[df["Order Status"] == "Complete"]
  df.rename(columns={
      "Execution Date": "Date",
      "Price": "Unit Price",
      "Quantity": "Shares",
      "Net Amount": "Amount",
  },
            inplace=True)
  df["Transaction Type"] = "Sell"
  clean_amount = lambda a: a.removeprefix("$").replace(",", "")
  for c in ["Unit Price", "Amount"]:
    df[c] = df[c].apply(clean_amount).astype(float)
  return df


def _from_releases_df(df: pd.DataFrame) -> pd.DataFrame:
  df = df[df["Status"] == "Complete"]
  df.rename(columns={
      "Vest Date": "Date",
      "Price": "Unit Price",
      "Net Share Proceeds": "Shares",
  },
            inplace=True)
  df["Transaction Type"] = "Buy"
  clean_amount = lambda a: a.removeprefix("$").replace(",", "")
  df["Unit Price"] = df["Unit Price"].apply(clean_amount).astype(float)
  df["Amount"] = (df["Unit Price"] * df["Shares"]).round(2)
  return df


def from_csv(fname: str) -> pd.DataFrame:
  df = pd.read_csv(fname)
  # Select GSU transactions only and exclude Dividend payouts.
  df = df[df["Plan"] == "GSU Class C"]
  # Split into releases (buys) and withdrawals (sales)
  # only.
  releases_df = df[df["Type"] == "Release"]
  withdrawals_df = df[df["Type"] == "Sale"]
  if releases_df.size != 0:
    df = _from_releases_df(releases_df)
  else:
    df = _from_withdrawals_df(withdrawals_df)
  # Convert the date from format like day-month-year to dd/mm/yyyy.
  df["Date"] = df["Date"].apply(
      lambda d: datetime.strptime(d, "%d-%b-%Y").strftime("%Y/%m/%d"))
  df["Shares"] = df["Shares"].abs()
  df["Amount"] = df["Amount"].abs()
  df["Commission"] = 0.0
  df["Security"] = "GOOG"
  df["Currency"] = "USD"
  df = df[common.DF_COLUMNS]
  return df
