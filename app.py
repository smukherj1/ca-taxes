import argparse

from pylib.rbc import load as rbc_load
from pylib.acb import export as acb_export


def dlr2acb(csv_in, csv_out):
  print("Reading {}".format(csv_in))
  df = rbc_load.fromCsv(csv_in)
  print("Exporting in ACB format to {}".format(csv_out))
  acb_export.toCsv(df, csv_out)


if __name__ == "__main__":
  p = argparse.ArgumentParser(description="Transaction Imported for Taxes")
  subparsers = p.add_subparsers(dest="subcommand")
  p_dlr2acb = subparsers.add_parser(
      "dlr2acb",
      help="Import RBC DI CSV transactions and tansform to ACB CSV.")
  p_dlr2acb.add_argument("-i", required=True, help="Input CSV file")
  p_dlr2acb.add_argument("-o", required=True, help="Output CSV file")
  args = p.parse_args()
  if args.subcommand == "dlr2acb":
    dlr2acb(args.i, args.o)
