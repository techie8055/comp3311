# COMP3311 21T3 Ass2 ... Python helper functions
# add here any functions to share between Python scripts 
# you must submit this even if you add nothing

def getProgram(db,code):
  cur = db.cursor()
  cur.execute("select * from Programs where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getProgramName(db,code):
  cur = db.cursor()
  cur.execute("select * from Programs where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info[2]


def getSubjectName(db,code):
  cur = db.cursor()
  cur.execute("select * from Subjects where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info[2]



def getSubject(db,code):
  cur = db.cursor()
  cur.execute("select * from Subjects where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStream(db,code):
  cur = db.cursor()
  cur.execute("select * from Streams where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStreamName(db,code):
  cur = db.cursor()
  cur.execute("select * from Streams where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info[2]


def getCourseNameFromSubject(db,code):
  cur = db.cursor()
  cur.execute("select * from Courses where subject = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info[2]



def getStudent(db,zid):
  cur = db.cursor()
  qry = """
  select p.*
  from   People p
         join Students s on s.id = p.id
  where  p.zid = %s
  """
  cur.execute(qry,[zid])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info


def getEnrolments(db,zid):
  cur = db.cursor()
  cur.execute("""
    SELECT
      pr.code,
      s.code,
      pr.name
      
    FROM 
      Program_enrolments pe
    JOIN  People p on p.id = pe.student
    JOIN Programs pr on pr.id = pe.program
    JOIN Stream_enrolments se on se.part_of = pe.id
    JOIN Streams s on s.id = se.stream
    Where  p.zid = %s
  """, (zid,))
  result = cur.fetchall()
  
  return(result)


def transcript(db,zid):
  cur = db.cursor()
  cur.execute("""
        SELECT 
        s.code,
        s.title,
        s.uoc,
        t.code,
        pe.mark,
        pe.grade
        FROM 
          Course_enrolments pe
        JOIN  People p on p.id = pe.student
        JOIN  Courses c on c.id = pe.course
        JOIN Subjects s on s.id = c.subject
        JOIN Terms t on t.id = c.term
        Where  p.zid = %s

        
        """, (zid,))
  result = cur.fetchall()
  
  return(result)

def updateDB(db):
  cur = db.cursor()
  cur.execute("""
        update requirements set min_req = 66 where id=322;
       
        """)
  cur.execute("""update requirements set min_req = 66 where id=318;""")
  
