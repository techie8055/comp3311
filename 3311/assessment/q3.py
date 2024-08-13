#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... print list of rules for a program or stream

import sys
import psycopg2
import re
from helpers import getProgram, getStream, getSubject,getProgramName, getSubjectName, getStreamName, getCourseNameFromSubject

# define any local helper functions here
# ...
def printHelper(min_req, max_req, name, rtype):
    if min_req is None and max_req is None:
        return f"all courses from {name}"
    elif min_req is not None and max_req is None:
        if (rtype == "uoc"):
          return f"Total UOC at least {min_req} UOC"
        elif (rtype == "elective"):
          return f"at least {min_req} UOC courses from {name}"
        elif (rtype == "free"):
          return f"at least {min_req} UOC of {name}"
        else:
          return f"at least {min_req}"
        
    elif min_req is None and max_req is not None:
        return f"up to {max_req}"
    elif min_req is not None and max_req is not None:
        if min_req < max_req:
            return f"between {min_req} and {max_req}"
        elif (rtype == "gened") :
          return (f"{min_req} UOC of General Education")
        elif (rtype == "stream"):
          return (f"{min_req} stream from {name}")
        elif (rtype == "elective"):
          return (f"{min_req} UOC courses from {name}")
        elif (rtype == "free"):
          return (f"{min_req} UOC of {name}")
        else:
            return (min_req)

def rtypeHelper(name, rtype,acadobjs):
  if (rtype == "core"):
    for i in acadobjs.split(','):
      if (i[0] == "{"):
        course_set = i.strip('{}')
        course_names = course_set.split(';')
        subject_name1 = getSubjectName(db, course_names[0])
        subject_name2 = getSubjectName(db, course_names[1])

        print(f"- {course_names[0]} {subject_name1}\n or {course_names[1]} {subject_name2}")
      
      else:
        subject_name = getSubjectName(db, i)
        print(f"- {i} {subject_name}")
  elif (rtype == "stream"):
    for i in acadobjs.split(','):
      stream_name = getStreamName(db, i)
      print(f"- {i} {stream_name}")
  elif (rtype == "elective"):    
      print(f"- {acadobjs}")


# req_types = ['stream', 'core', 'elective','gened','free']
# ### set up some globals

usage = f"Usage: {sys.argv[0]} (ProgramCode|StreamCode)"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
code = sys.argv[1]
if len(code) == 4:
  codeOf = "program"
elif len(code) == 6:
  codeOf = "stream"
else:
  print("Invalid code")
  exit(1)

try:
  db = psycopg2.connect("dbname=ass2")
  if codeOf == "program":
    progInfo = getProgram(db,code)
    
    if not progInfo:
      print(f"Invalid program code {code}")
      exit(1)
    #print(progInfo)  #debug

    # List the rules for Program
    # ... add your code here ...
    print(f"{code} {getProgramName(db,code)}")
    print("Academic Requirements:")

    reqqry = f"""
    SELECT *
FROM Requirements
WHERE for_program = (SELECT id FROM Programs WHERE code = %s);
    """

    with db.cursor() as cursor:
        cursor.execute(reqqry, (code,))
        results = cursor.fetchall()  # Use fetchall() to get all rows
        
    for result in results:
      # print(result)
      id, name, rtype, min_req, max_req, acadobjs, for_stream, for_program = result
      print(printHelper(min_req, max_req, name, rtype))
      rtypeHelper(name,rtype,acadobjs)

  elif codeOf == "stream":
    
    
    strmInfo = getStream(db,code)
    if not strmInfo:
      print(f"Invalid stream code {code}")
      exit(1)
    #print(strmInfo)  #debug
    print(f"{code} {getStreamName(db,code)}")
    print("Academic Requirements:")
    reqqry = f"""
    SELECT *
FROM Requirements
WHERE for_stream = (SELECT id FROM Streams WHERE code = %s);
    """

    with db.cursor() as cursor:
      cursor.execute(reqqry, (code,))
      results = cursor.fetchall()  # Use fetchall() to get all rows
  
    for result in results:
      # print(result)
      id, name, rtype, min_req, max_req, acadobjs, for_stream, for_program = result
      print(printHelper(min_req, max_req, name, rtype))
      rtypeHelper(name,rtype,acadobjs)
except Exception as err:
  print(err)
finally:
  if db:
    db.close()
