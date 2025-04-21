import pandas as pd


def ToCsv(df: pd.DataFrame, fname: str):
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
