import pandas as pd
"""
Expect Data Frame with columns:
- Date: dd/mm/yyyy
- Security: Ticker or stock symbol.
- Transaction Type: Sell, Buy.
- Amount: Total transaction amount, i.e., Unit Price x Shares.
- Unit Price: Price of an individual security.
- Shares: Number of units of security in the transaction.
- Commission: Commission paid.
- Currency: Transaction currency, e.g., CAD, USD, etc.
"""


def toCsv(df: pd.DataFrame, fname: str):
  df["Price in Foreign Currency?"] = df["Currency"].apply(
      lambda c: "Yes" if c != "CAD" else "No")
  df["Commission in Foreign Currency?"] = df["Currency"].apply(
      lambda c: "Yes" if c != "CAD" else "No")
  df["Exchange Rate"] = df["Currency"].apply(lambda c: c if c != "CAD" else "")
  columns = [
      "Security",
      "Date",
      "Transaction Type",
      "Amount",
      "Shares",
      "Commission",
      "Price in Foreign Currency?",
      "Commission in Foreign Currency?",
      "Exchange Rate",
  ]
  df = df[columns]
  df.to_csv(fname, index=False)
