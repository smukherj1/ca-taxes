import pandas as pd
from ..common import common


def to_csv(df: pd.DataFrame, fname: str):
  df = common.reorder_df_by(df, "Date")
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
