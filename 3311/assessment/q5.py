#!/usr/bin/python3
# COMP3311 21T3 Ass2 ... progression check for a given student

import sys
import psycopg2
import re
from helpers import getStudent, getProgram, getStream, updateDB, transcript

# define any local helper functions here
def printHelper(item,reqString):
  global noFailCount
  global markTotal
  global subjectCount

  if item[5] in countUOCList:
        noFailCount = noFailCount + item[2]

  if item[4] is not None:
        subjectCount = subjectCount + item[2]

        if item[5] in wamCountList:
            markTotal = markTotal + (item[2] * item[4])

        if item[5] in failList:
            print(f"{item[0]} {item[3]} {item[1][:31]:<32s}{item[4]:>3} {item[5]:>2s}   fail ")
        elif item[5] in unrsList:

            print(f"{item[0]} {item[3]} {item[1][:31]:<32s}{item[4]:>3} {item[5]:>2s}   unrs ")
        else:
            print(f"{item[0]} {item[3]} {item[1][:31]:<32s}{item[4]:>3} {item[5]:>2s}  {item[2]:2d}uoc {reqString}")
  elif item[4] is None and item[5] in unrsList:
        print(f"{item[0]} {item[3]} {item[1][:31]:<32s} - {item[5]:>2s}  unrs ")
  else:
        print(f"{item[0]} {item[3]} {item[1][:31]:<32s} - {item[5]:>2s}  {item[2]:2d}uoc {reqString}")

def checkInFreeList(input_code, code_string):
    pattern_string = ''
    for char in code_string:
        if char == '#':
            pattern_string += r'\d'
        elif char == ',':
            pattern_string += r'|'
        else:
            pattern_string += re.escape(char)
    

    pattern = re.compile(pattern_string)

    return bool(pattern.search(input_code))

# Rest of your code...

### set up some globals
subjectCount = 0
markTotal = 0
noFailCount = 0
elecUOC = 0
freeUOC = 0
genUOC = 0
wamCountList = ["HD","DN","CR","PS","AF","FL","UF","E","F"]
failList= ["AF","FL","UF","E","F"]
unrsList= ["AS", "AW", "PW", "NA", "RD", "NF", "NC", "LE", "PE", "WD", "WJ"]
countUOCList =  ["A", "B", "C", "D", "HD", "DN", "CR", "PS", "XE", "T", "SY", "EC", "RC"]
wamCountPassedList = ["HD","DN","CR","PS"]
noUOCList = ['AF', 'FL', 'UF', 'E', 'F', 'AS', 'AW', 'PW', 'NA', 'RD', 'NF', 'NC', 'LE', 'PE', 'WD', 'WJ']

usage = f"Usage: {sys.argv[0]} zID [Program Stream]"
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
  print("Invalid student ID")
  exit(1)

progCode = None
strmCode = None

if argc == 4:
  progCode = sys.argv[2]
  strmCode = sys.argv[3]

# manipulate database

try:
  db = psycopg2.connect("dbname=ass2")
  # updateDB(db)
  stuInfo = getStudent(db,zid)
  if not stuInfo:
    print(f"Invalid student id {zid}")
    exit(1)
  #print(stuInfo) # debug

  if progCode:
    progInfo = getProgram(db,progCode)
    if not progInfo:
      print(f"Invalid program code {progCode}")
      exit(1)
    #print(progInfo)  #debug

  if strmCode:
    strmInfo = getStream(db,strmCode)
    if not strmInfo:
      print(f"Invalid program code {strmCode}")
      exit(1)
    #print(strmInfo)  #debug
  
  coreList = []
  electiveList = []
  freeList = []

  
  reqqry = f"""
    SELECT *
FROM Requirements
WHERE for_stream = (SELECT id FROM Streams WHERE code = %s);
    """
  reqqry2 = f"""
    SELECT *
FROM Requirements
WHERE for_program = (SELECT id FROM Programs WHERE code = %s);
    """

   
  with db.cursor() as cursor:
    
    cursor.execute(reqqry, (strmCode,))
    results = cursor.fetchall()  # Use fetchall() to get all rows

    cursor.execute(reqqry2, (progCode,))
    results2 = cursor.fetchall()
    
    
    for item in results:
      
      if (item[2] == "core" and item[2] not in noUOCList):
        coreList.append((item[1], item[5]))
      elif (item[2] == "elective" and item[2] not in noUOCList):
        if (item[3] > elecUOC):
          elecUOC = elecUOC + item[3]
        electiveList.append((item[1], item[5]))
        
      elif (item[2] == "free" and item[2] not in noUOCList):
        
        if (item[3] > freeUOC):
          freeUOC = freeUOC + item[3]
        freeList.append((item[1], item[5]))
      elif (item[2] == "gened" and item[2] not in noUOCList):
        genUOC = genUOC + item[3]
      
        

    
    for item in results2:
      if (item[2] == "core" and item[2] not in noUOCList):
        coreList.append((item[1], item[5]))
      elif (item[2] == "elective" and item[2] not in noUOCList):
        if (item[3] > elecUOC):
          elecUOC = elecUOC + item[3]
       
        electiveList.append((item[1], item[5]))
      elif (item[2] == "free" and item[2] not in noUOCList):
        if (item[3] > freeUOC):
          freeUOC = freeUOC + item[3]
        
        freeList.append((item[1], item[5]))
      elif (item[2] == "gened" and item[2] not in noUOCList):
        genUOC = genUOC + item[3]
   
    
    print(freeList)
    print(electiveList)
    data = sorted(transcript(db, zid), key=lambda item: (item[3], item[0]))
    for item in data:
      printed_flag = False
      if (item[5] in noUOCList):

        printHelper(item,reqString)
          
       
        # Modify coreList
      else:
        for i, tup in enumerate(coreList):
            if item[0] in tup[1]:
                reqString = tup[0]
                printHelper(item, reqString)
                values_list = tup[1].split(',')
                if item[0] in values_list:
                    values_list.remove(item[0])
                    modified_string = ','.join(values_list)
                    coreList[i] = (tup[0], modified_string)
                    if modified_string == '':
                        coreList.pop(i)
                printed_flag = True

        # Modify electiveList
        for i, tup in enumerate(electiveList):
          
          if (printed_flag == False):
            if checkInFreeList(item[0], tup[1]) and (elecUOC > 0):
                
                printed_flag = True
                elecUOC = elecUOC - item[2]
                print(elecUOC)
                reqString = tup[0]
                printHelper(item, reqString)
                

        # Modify freeList
        for i, tup in enumerate(freeList):
          if (printed_flag == False):
            
            if (genUOC > 0):
              printed_flag = True
              genUOC = genUOC - item[2]
              reqString = "General Education"
              printHelper(item, reqString)
            elif ( freeUOC > 0): #logic here is bad
              printed_flag = True
              freeUOC = freeUOC - item[2]
              reqString = tup[0]
              printHelper(item, reqString)
            elif (genUOC == 0 & elecUOC == 0):
              printed_flag = True
              
              reqString = ""
              printHelper(item, reqString)
              
                

    # Print the modified lists
    # print(coreList)
    # print(electiveList)
    # print(freeList)
    

except Exception as err:
  print("DB error: ", err)
finally:
  if db:
    db.close()

