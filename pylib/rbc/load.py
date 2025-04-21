import pandas as pd
from datetime import datetime


def from_csv(fname: str) -> pd.DataFrame:
  df = pd.read_csv(fname)
  # Reverse order of transactions to list them in ascending order
  # by date.
  df = df.iloc[::-1]
  # Filter out only the DLR buy/sell transactions.
  df = df[df["Symbol"] == "DLR"]
  df = df[df["Activity"].isin(["Buy", "Sell"])]
  # Rename some columns to the ACB website import format.
  df.rename(columns={
      "Symbol": "Security",
      "Activity": "Transaction Type",
      "Quantity": "Shares",
      "Price": "Unit Price",
      "Value": "Amount",
  },
            inplace=True)
  # Convert the date from format like Monday day, Year to dd/mm/yyyy.
  df["Date"] = df["Date"].apply(
      lambda d: datetime.strptime(d, "%B %d, %Y").strftime("%d/%m/%Y"))
  df["Shares"] = df["Shares"].abs()
  df["Amount"] = df["Amount"].abs()
  df["Commission"] = 0.0
  keep_columns = [
      "Date", "Security", "Transaction Type", "Amount", "Unit Price", "Shares",
      "Commission", "Currency"
  ]
  df = df[keep_columns]
  return df
