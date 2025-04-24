import pandas as pd
from datetime import datetime
from ..common import common


def dlr_from_csv(fname: str) -> pd.DataFrame:
  df = from_csv(fname)
  # Filter out only the DLR buy/sell transactions.
  df = df[df["Security"] == "DLR"]
  df = df[df["Transaction Type"].isin(["Buy", "Sell"])]
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
  # Convert the date from format like Monday day, Year to yyyy/mm/dd.
  df["Date"] = df["Date"].apply(
      lambda d: datetime.strptime(d, "%B %d, %Y").strftime("%Y/%m/%d"))
  # Stable sort transactions in increasing order by Date.
  df = common.reorder_df_by(df, "Date")
  df["Shares"] = df["Shares"].abs()
  df["Amount"] = df["Amount"].abs()
  df["Commission"] = 0.0
  df = df[common.DF_COLUMNS]
  return df
