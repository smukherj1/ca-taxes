import argparse

from pylib.rbc import load as rbc_load
from pylib.acb import export as acb_export
from pylib.gsu import load as gsu_load
from pylib.common import common
from datetime import datetime


def dlr2acb(csv_files_in: list[str], csv_out: str):
  dfs = []
  for cf_in in csv_files_in:
    print("Loading {}".format(cf_in))
    dfs.append(rbc_load.dlr_from_csv(cf_in))
    print("Exporting in ACB format to {}".format(csv_out))
  df = common.merge_dfs(dfs)
  acb_export.to_csv(df, csv_out)


def gsu2acb(csv_files_in: list[str], csv_out: str):
  dfs = []
  for cf_in in csv_files_in:
    print("Loading {}".format(cf_in))
    dfs.append(gsu_load.from_csv(cf_in))
  df = common.merge_dfs(dfs)
  acb_export.to_csv(df, csv_out)


def aggdist(csv_files_in: list[str], csv_out: str):
  dfs = []
  for cf_in in csv_files_in:
    print("Loading {}".format(cf_in))
    dfs.append(rbc_load.from_csv(cf_in))
  df = common.merge_dfs(dfs)
  df["Year"] = df["Date"].apply(
      lambda d: datetime.strptime(d, "%Y/%m/%d").strftime("%Y")).astype(int)
  df = df[df["Transaction Type"] == "Distribution"]
  df = df[["Year", "Security", "Amount"]]
  df = df.groupby(by=["Year", "Security"], as_index=False).sum()
  df.to_csv(csv_out, index=False)


if __name__ == "__main__":
  p = argparse.ArgumentParser(description="Transaction Imported for Taxes")
  subparsers = p.add_subparsers(dest="subcommand")

  p_dlr2acb = subparsers.add_parser(
      "dlr2acb",
      help=
      "Import RBC DI CSV transactions and transform to CSV importable into adjustedcostbase.ca."
  )
  p_dlr2acb.add_argument(
      "-i",
      required=True,
      action="append",
      help="Input CSV file. Can be specified multiple times.")
  p_dlr2acb.add_argument("-o", required=True, help="Output CSV file.")

  p_gsu2acb = subparsers.add_parser(
      "gsu2acb",
      help=
      "Import Morgan Stanley GSU transactions and transform CSV importable into adjustedcostbase.ca."
  )
  p_gsu2acb.add_argument(
      "-i",
      required=True,
      action="append",
      help="Input CSV file. Can be specified multiple times.")
  p_gsu2acb.add_argument("-o", required=True, help="Output CSV file.")

  p_aggdist = subparsers.add_parser(
      "aggdist",
      help=
      "Import RBC DI CSV transactions and aggregate distributions by year and symbol to estimate T3 slip values. Helps decide how much to contribute to RRSP."
  )
  p_aggdist.add_argument(
      "-i",
      required=True,
      action="append",
      help="Input CSV file. Can be specified multiple times.")
  p_aggdist.add_argument("-o", required=True, help="Output CSV file.")

  args = p.parse_args()
  if args.subcommand == "dlr2acb":
    dlr2acb(args.i, args.o)
  elif args.subcommand == "gsu2acb":
    gsu2acb(args.i, args.o)
  elif args.subcommand == "aggdist":
    aggdist(args.i, args.o)
  else:
    raise RuntimeError("Unsupported command: {}".format(args.subcommand))
