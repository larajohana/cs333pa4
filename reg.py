#----------------------------------------------------------------------
# reg.py
# Authors: Maria Aguirre, Johana Lara
#----------------------------------------------------------------------

import flask
import database
import sys

#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')


def get_courses(search):
    _, table = database.get_courses(search)
    courses = []

    try:
        if _:
            raise Exception(_, table)

        if table is not None:
            for row in table:
                classid, dept, courseid, area, title =(
                    row[0], row[1], row[2], row[3], row[4])
                course = (classid, dept, courseid, area, title)
                courses.append(course)

        return courses

    except Exception as table:
        print(table,file = sys.stderr)
        sys.exit(2)

def get_details(classid):
    details = []
    _, details = database.get_details(classid)
    try:
        if _:
            raise Exception(_, details)
    except Exception as details:
        print(details,file = sys.stderr)
        sys.exit(2)

    return details

def check_req(dept, coursenum, area, title):
    if dept is None:
        dept = ''
    if area is None:
        area = ''
    if coursenum is None:
        coursenum = ''
    if title is None:
        title = ''

    return dept, coursenum, area, title

#----------------------------------------------------------------------

@app.route('/', methods = ['GET'])
def search_form():
    html_code = flask.render_template('searchform.html')
    response = flask.make_response(html_code)
    return response


@app.route('/searchform', methods = ['GET'])
def course():
    dept = flask.request.args.get('dept')
    coursenum = flask.request.args.get('coursenum')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')

    dept, coursenum, area, title = check_req(
        dept, coursenum, area, title)

    search = {"dept": dept, "coursenum": coursenum,
                "area": area, "title": title}

    courses = []
    courses = get_courses(search)


    html_code = flask.render_template(
            'courses.html', courses = courses)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------



@app.route('/regdetails', methods = ['GET'])
def regdetails():
    classid = flask.request.args.get('classid')
    if not classid:
        return flask.redirect(flask.url_for('error',
                                        message='missing classid'))
    if not classid.isdigit():
        return flask.redirect(flask.url_for('error',
                                        message='non-integer classid'))

    try:
        details = []
        details = get_details(classid)

        html_code = flask.render_template(
            'regdetails.html', details=details, classid=classid)

        response = flask.make_response(html_code)
        return response
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        error_message = [
    'A server error occurred. Please contact the system administrator.']
        return flask.render_template('error.html', 
                                     message=error_message)
        


#----------------------------------------------------------------------

@app.route('/error')
def error():
    # Get the error message from the query parameters
    error_message = flask.request.args.get('message', 
                                           'Unknown Error')

    # error template with the error message
    html_code = flask.render_template('error.html', 
                                      message=error_message)

    response = flask.make_response(html_code)
    return response