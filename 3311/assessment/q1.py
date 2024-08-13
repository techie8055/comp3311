#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track proportion of overseas students

import sys
import psycopg2
import re

# define any local helper functions here
# ...

### set up some globals

db = None

### process command-line args


try:
  db = psycopg2.connect("dbname=ass2")

  # show term, #locals, #internationals, fraction
  print(f"Term {'#Locl'} {'#Intl'} {'Proportion'}")
  with db.cursor() as cursor:
  
            for year in range(19, 24):
              for term in range(0, 4):
                term_code = f"{year}T{term}"
                cursor.execute("""
                SELECT 
                  t.code,
                  COUNT( DISTINCT CASE WHEN s.status = 'INTL' THEN pe.student END) as intl,
                  COUNT( DISTINCT CASE WHEN s.status != 'INTL' THEN pe.student END) as aust

                FROM Students s
                JOIN Program_enrolments pe ON s.id = pe.student
                JOIN Terms t ON pe.term = t.id
                WHERE
                 t.code = %s 
                GROUP BY
                  t.code
                """,(term_code,))
                result = cursor.fetchone()
       
                if result:               
                  term_code, intl, aust = result
                  proportion = aust/intl
                  print(f"{term_code} {aust:6d} {intl:6d} {proportion:6.1f}")
               
except Exception as err:
  print(err)
finally:
  if db:
    db.close()
