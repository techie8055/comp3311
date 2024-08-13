#!/usr/bin/python3
# COMP3311 22T3 Ass2 ... print a transcript for a given student

import sys
import psycopg2
import re
from helpers import getStudent, transcript, getEnrolments

# define any local helper functions here

### set up some globals

usage = f"Usage: {sys.argv[0]} zID"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
zid = sys.argv[1]
if zid[0] == 'z':
  zid = zid[1:8]
digits = re.compile("^\d{7}$")
if not digits.match(zid):
  print(f"Invalid student ID {zid}")
  exit(1)

# manipulate database

try:
  db = psycopg2.connect("dbname=ass2")
  
  
  stuInfo = getStudent(db,zid)
  if (stuInfo is None):
    print(f"Invalid student ID {zid}")
    exit(1)

  enrolment = getEnrolments(db,zid)
  enrolment = enrolment[-1]

  
  
  print(f"{stuInfo[1]} {stuInfo[2]}, {stuInfo[3]}")
  print(f"{enrolment[0]} {enrolment[1]} {enrolment[2]}")
 

  
  
  if not stuInfo:
    print(f"Invalid student ID {zid}")
    exit(1)
  data = sorted(transcript(db, zid), key=lambda item: (item[3], item[0]))  
  subjectCount = 0
  markTotal = 0
  noFailCount = 0
  wamCountList = ["HD","DN","CR","PS","AF","FL","UF","E","F"]
  failList= ["AF","FL","UF","E","F"]
  unrsList= ["AS", "AW", "PW", "NA", "RD", "NF", "NC", "LE", "PE", "WD", "WJ"]
  countUOCList =  ["A", "B", "C", "D", "HD", "DN", "CR", "PS", "XE", "T", "SY", "EC", "RC"]
  wamCountPassedList = ["HD","DN","CR","PS"]
  for item in data:
    
    if (item[5] in countUOCList):
        noFailCount = noFailCount + item[2]

    if (item[4] is not None):
      subjectCount = subjectCount+ item[2]
      
      

      if (item[5] in wamCountList):
        
          

        
        markTotal = markTotal + (item[2] * item[4])

      if (item[5] in failList):
        print(f"{item[0]} {item[3]} {item[1][:31]:<32s}{item[4]:>3} {item[5]:>2s}   fail")
      elif (item[5] in unrsList):
        print(f"{item[0]} {item[3]} {item[1][:31]:<32s}{item[4]:>3} {item[5]:>2s}   unrs")
      else:
        print(f"{item[0]} {item[3]} {item[1][:31]:<32s}{item[4]:>3} {item[5]:>2s}  {item[2]:2d}uoc")
    elif (item[4] is None and item[5] in unrsList):
      print(f"{item[0]} {item[3]} {item[1][:31]:<32s} - {item[5]:>2s}  unrs")
    else:
      print(f"{item[0]} {item[3]} {item[1][:31]:<32s} - {item[5]:>2s}  {item[2]:2d}uoc")


  wam = markTotal / subjectCount
  print(f"UOC = {noFailCount}, WAM = {wam:.1f}")
 


# Now you can use the 'result' variable outside the 'with' block
# Print transcript for the student
# ... add your code here 
 
except Exception as err:
  print("DB error: ", err)
finally:
  if db:
    db.close()

