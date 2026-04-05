import pandas as pd
from datetime import datetime
from ..common import common

# Mapping from RBC DI transaction type to ACB website transaction type.
_activity_map = {
    "Buy": "Buy",
    "Sell": "Sell",
    "Dividends": "Reinvested Dividend",
}


def di_from_csv(fname: str) -> pd.DataFrame:
  df = from_csv(fname)
  activity_types = _activity_map.keys()
  df = df[df["Transaction Type"].isin(activity_types)]
  df["Transaction Type"] = df["Transaction Type"].map(_activity_map)
  return df


def from_csv(fname: str) -> pd.DataFrame:
  df = pd.read_csv(fname)
  # Rename some columns to the ACB website import format.
  df.rename(columns={
      "Symbol": "Security",
      "Activity": "Transaction Type",
      "Quantity": "Shares",
      "Price": "Unit Price",
      "Value": "Amount",
  },
            inplace=True)
  # Convert the date from format like 01-Jan-23 to yyyy/mm/dd.
  df["Date"] = df["Date"].apply(
      lambda d: datetime.strptime(d, "%d-%b-%y").strftime("%Y/%m/%d"))
  # Stable sort transactions in increasing order by Date.
  df = common.reorder_df_by(df, "Date")
  df["Shares"] = df["Shares"].abs()
  df["Amount"] = df["Amount"].abs()
  df["Commission"] = 0.0
  df = df[common.DF_COLUMNS]
  return df
