from PyPDF2 import PdfReader

files = ["rbc.pdf", "gsu_buy.pdf", "gsu_sell.pdf"]
for f in files:
  r = PdfReader(f)
  print("{} -> {} pages.".format(f, len(r.pages)))
  t = r.pages[0].extract_text()
  print("{}, page 0, text size {}.".format(f, len(t)))
  o = f.removesuffix(".pdf") + ".txt"
  with open(o, "w") as ofp:
    ofp.write(t)
