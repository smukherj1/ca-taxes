import pandas as pd
from datetime import datetime


def from_csv(fname: str) -> pd.DataFrame:
  df = pd.read_csv(fname)
  # Cannonicalize the Date column name.
  if "Execution Date" in df.columns:
    df.rename(columns={"Execution Date": "Date"}, inplace=True)
  elif "Vest Date" in df.columns:
    df.rename(columns={"Vest Date": "Date"}, inplace=True)
  # Select GSU transactions only and exclude Dividend payouts.
  df = df[df["Plan"] == "GSU Class C"]

  clean_amount = lambda a: a.removeprefix("$").replace(",", "")
  df["Price"] = df["Price"].apply(clean_amount)
  return df
