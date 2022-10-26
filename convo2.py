#!/usr/bin/python
import sys
import re
import tools
import csv

ver = "0.1"

print("ConvoTwo v" + ver)
print("Using Python " + sys.version + "\n")

if sys.version_info[0] < 3:
  tools.error_exit("Must be using Python 3. Try py -3!")

files = ["fictional-051022", "conversations-051022"]

for file in files:
  linecount = 0
  getid2 = False
  id1 = ""
  id2 = ""
  
  with open("docs/" + file + "-output.tsv", encoding="utf8", mode="w") as w:
    writer = csv.writer(w, delimiter='\t', lineterminator='\n')
    w.write("ID1\tID2\tturn_all\tturn_no\tword\tsentence\n")
    with open("docs/" + file + ".txt", encoding="utf8", mode="r") as f:
      lines = f.readlines()
      turns = []
      for line in lines:
        linecount = linecount + 1
        if linecount == 1:
          continue
        if re.match(r"[A-Z]\d*$", line):
          for turn in turns:
            writer.writerow([id1, id2, turn_no, turn["no"], turn["word"], turn["sentence"]])
          turn_no = 0
          turns = []
          id1 = line.replace("\n", "")
          getid2 = True
          continue
        if getid2 == True:
          id2 = line.replace("\n", "")
          getid2 = False
          continue
        turn_no = turn_no + 1
        modline = line.replace("\"", "")
        # Make sentences from sentence parts where ... is followed by an uppercase letter
        modline = re.sub(r"\.\.\. ([A-Z])", r". \1", modline)
        # Remove the rest of ...
        modline = modline.replace("....", "").replace("...", "")
        # Add a trailing full stop where there's none
        modline = re.sub(r"[A-Z …]$", ".", modline)
        turns.append({
          "no": turn_no,
          "word": len(line.split(" ")),
          "sentence": modline.count(".") + modline.count("!") + modline.count("?")
        })
        
  print(f"{file}: Processed {linecount} lines.")
