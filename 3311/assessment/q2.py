#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track satisfaction in a given subject

import sys
import psycopg2
import re

from helpers import getSubject

# define any local helper functions here
# ...

### set up some globals

usage = f"Usage: {sys.argv[0]} SubjectCode"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
subject = sys.argv[1]
check = re.compile("^[A-Z]{4}[0-9]{4}$")
if not check.match(subject):
  print("Invalid subject code")
  exit(1)

try:
  db = psycopg2.connect("dbname=ass2")
  subjectInfo = getSubject(db,subject)
  if not subjectInfo:
      print(f"Invalid subject code {code}")
      exit(1)
  id , course, name, uoc, career, owner = subjectInfo
  print(course, name)
  

  # List satisfaction for subject over time

  # ... add your code here ...
  print(f"Term {'Satis'} {'#resp'} {'#stu'} {'Convenor'}")
  with db.cursor() as cursor:
  
            for year in range(19, 24):
              for term in range(0, 4):
                term_code = f"{year}T{term}"
                cursor.execute("""
                SELECT 
                t.code,
                c.satisfact as Satisfaction,
                c.nresponses as Responses,
                COUNT (DISTINCT ce.student) as enrolled_students,
                p.full_name as Convenor

                FROM
                Courses c
                JOIN Subjects s ON c.subject = s.id
                JOIN Terms t ON c.term = t.id
                LEFT JOIN Course_enrolments ce ON c.id = ce.course  
                JOIN People p ON c.convenor = p.id
                WHERE
                t.code = %s AND s.code = %s
                GROUP BY
                  t.code, Satisfaction, Responses, p.full_name
                """,(term_code,subject))
                result = cursor.fetchone()
               
                if (result):  
                  flag = 0
                  term, satis, resp, stu, convenor = result
                  if (term is None):
                    term = '?'
                    flag = 1
                  if (satis is None):
                    satis = '?'
                    flag = 1
                  if (resp is None):
                    resp = '?'
                    flag = 1
                  if (convenor is None):
                    convenor = '?'
                    flag = 1

                  if (flag == 1):
                    print(f"{term} {satis:>{6}} {resp:>{6}} {stu:>{6}} {convenor}")
                  else:
                    print(f"{term} {satis:6d} {resp:6d} {stu:6d} {convenor}")

except Exception as err:
  print(err)
finally:
  if db:
    db.close()
