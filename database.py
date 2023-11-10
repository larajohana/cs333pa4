#--------------------------------------------------------------------
# database.py
# Authors: Maria Aguirre, Johana Lara
#--------------------------------------------------------------------

import sys
import contextlib
import sqlite3

#--------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=ro'

#--------------------------------------------------------------------
def escape_special_characters(search_string):
    # Replacing % with \% and _ with \_
    return search_string.replace('%', '\%').replace('_', '\_')

def get_courses(search):

    stmt_str =  "SELECT classid, dept, coursenum, area, title "
    stmt_str += "FROM classes, crosslistings, courses "
    stmt_str += "WHERE classes.courseid = courses.courseid "
    stmt_str += "AND classes.courseid = crosslistings.courseid "

    id = []

    if search.get('dept'):
        escaped_dept = escape_special_characters(search.get('dept'))
        stmt_str += "AND crosslistings.dept LIKE ? ESCAPE '\\'"
        id.append('%' + escaped_dept + '%')

    if search.get('coursenum'):
        escaped_coursenum = escape_special_characters(search.get
                                                      ('coursenum'))
        stmt_str += "AND coursenum LIKE ? ESCAPE '\\'"
        id.append('%' + escaped_coursenum + '%')

    if search.get('area'):
        escaped_area = escape_special_characters(search.get('area'))
        stmt_str += "AND courses.area LIKE ? ESCAPE '\\'"
        id.append('%' + escaped_area + '%')

    if search.get('title'):
        escaped_title = escape_special_characters(search.get('title'))
        stmt_str += "AND courses.title LIKE ? ESCAPE '\\'"
        id.append('%' + escaped_title + '%')

    try:
        # Connection setup with database
        with sqlite3.connect(
            DATABASE_URL, isolation_level = None, uri = True
            ) as connection:

            with contextlib.closing(connection.cursor()) as cursor:

                stmt_str += "ORDER BY dept, coursenum, classid ASC"
                cursor.execute(stmt_str, id)

                table = cursor.fetchall()
                return 0, table

    except Exception as ex:
        print(ex,file = sys.stderr)
        return 1, ex
        sys.exit(1)

#--------------------------------------------------------------------

def get_details(search):

    try:
        # Connection setup with database
        with sqlite3.connect(
            DATABASE_URL, isolation_level = None, uri = True
            ) as connection:

            with contextlib.closing(connection.cursor()) as cursor:

                classid = []
                classid.append(search)

                # Course logistics query
                logistics = ("SELECT days, starttime, endtime, bldg, "
                             "roomnum, courses.courseid ")
                logistics += "FROM classes, courses, crosslistings "
                logistics += "WHERE classes.courseid ="\
                    " courses.courseid "
                logistics += ("AND classes.courseid = "
                              "crosslistings.courseid ")
                logistics += "AND classid = ? "

                cursor.execute(logistics, classid)
                log_table = cursor.fetchone()
                (days, starttime, endtime, bldg, roomnum,
                 courseid) = log_table

                classid_str = str(search)
                days = str(days)
                starttime = str(starttime)
                endtime = str(endtime)
                bldg = str(bldg)
                roomnum = str(roomnum)
                courseid = str(courseid)

                # Department and course number query
                coursename = "SELECT dept, coursenum "
                coursename += ("FROM classes, "
                               "courses, crosslistings ")
                coursename += ("WHERE classes.courseid "
                               "= courses.courseid ")
                coursename += ("AND classes.courseid "
                                "= crosslistings.courseid ")
                coursename += "AND classid = ? "

                cursor.execute(coursename, classid)
                course_table = cursor.fetchall()

                dept_and_number = []
                for dept, coursenum in course_table:
                    dept_and_number.append(
                        str(dept) + " " + str(coursenum))

                # Department and course number query
                details = "SELECT area, title, descrip, prereqs "
                details += "FROM courses, classes, crosslistings "
                details += "WHERE classes.courseid = courses.courseid "
                details +=  (
                    "AND classes.courseid = crosslistings.courseid ")
                details += "AND classid = ? "

                cursor.execute(details, classid)
                det_table = cursor.fetchone()
                area, title, descrip, prereqs = det_table

                if area is None:
                    area.append("(None) ")
                else:
                    area = str(area)

                title = str(title)
                descrip = str(descrip)

                if prereqs is None:
                    prereqs.append("(None are listed)")
                else:
                    prereqs = str(prereqs)

                # Professor query
                prof  = "SELECT profname "
                prof += "FROM profs, coursesprofs, classes "
                prof += "WHERE profs.profid = coursesprofs.profid "
                prof += "AND coursesprofs.courseid = classes.courseid "
                prof += "AND classid = ? "

                cursor.execute(prof, classid)
                prof_names = cursor.fetchall()

                if prof_names:
                    for prof in prof_names:
                        prof_names = prof[0]
                else:
                    prof_names = " "

                course_details = [
                    classid_str, days, starttime,
                    endtime, bldg, roomnum,dept_and_number,
                    area,title, descrip, prereqs, prof_names, courseid]
                return 0, course_details

    except Exception as ex:
        print(ex,file = sys.stderr)
        return 1, ex
        sys.exit(1)
