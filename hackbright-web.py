from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/student-search")
def get_student_form():
    """Show form to search for a student."""

    return render_template("student_search.html")
 

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)
    return html

@app.route("/student-add")
def add_new_student():
    """Show new student form"""

    return render_template("new_student.html")

@app.route("/student-confirmation", methods=['POST'])
def added_student():
    """Confirm added new student"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    github = request.form.get('github')
    hackbright.make_new_student(fname, lname, github)

    return render_template("student_confirmation.html",
                            fname=fname,
                            lname=lname,
                            github=github)

@app.route("/project")
def show_project_info():
    """Show title, description, and max grade of a project"""

    title = request.args.get('title')
    title, description, max_grade = hackbright.get_project_by_title(title)

    return render_template("project_info.html",
                            title=title,
                            description=description,
                            max_grade=max_grade)




if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
