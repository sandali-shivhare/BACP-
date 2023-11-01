from flask import Flask, render_template, request
import csv
from academic_curriculum import Course, blue_whale_algorithm

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csv_data = request.form['csv-data']
        courses = read_courses_from_csv_string(csv_data)
        population_size = 30
        max_iterations = 100
        curriculum = blue_whale_algorithm(courses, population_size, max_iterations)

        return render_template('index.html', curriculum=curriculum)

    return render_template('index.html')

def read_courses_from_csv_string(csv_data):
    courses = []
    reader = csv.reader(csv_data.splitlines())

    for row in reader:
        name = row[0].strip()
        credits = int(row[1].strip())
        period = int(row[2].strip())
        duration = int(row[3].strip())

        prerequisites = [int(x.strip()) for x in row[4].split()] if row[4].strip() else []

        courses.append(Course(name, credits, period, duration, prerequisites))

    return courses

if __name__ == '__main__':
    app.run(port=5000)
