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
DF_COLUMNS = [
    "Date", "Security", "Transaction Type", "Amount", "Unit Price", "Shares",
    "Commission", "Currency"
]


def reorder_df_by(df: pd.DataFrame,
                  colname: str,
                  ascending: bool = True) -> pd.DataFrame:
  s = df[colname]
  if (s.is_monotonic_increasing and ascending) or (s.is_monotonic_decreasing
                                                   and not ascending):
    return df
  if not s.is_monotonic_increasing and not s.is_monotonic_decreasing:
    raise RuntimeError(
        "rows were not already sorted by column {}".format(colname))
  df[colname] = s[::-1]
  return df


def merge_dfs(dfs: list[pd.DataFrame]) -> pd.DataFrame:
  df = pd.concat(dfs, ignore_index=True)
  return df.sort_values(by="Date", kind="mergesort")
