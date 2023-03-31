from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Contest

app = Flask(__name__)
app.secret_key = b'secret-this-is-a-secret-key-24525-235-%^$%_@#%@_535NNVUbbijw_jigr'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        full_name: str = request.form['full_name']
        roll_no: int = int(request.form['roll'])
        section: str = request.form['section']
        shift: str = request.form['shift']

        response: str = request.form['response']

        word_count: int = len(response.split(' '))
        print(
            '\n\n\n word_count: ', word_count, '\n\n\n'
        )

        unique_id = request.form['unique_id']

        contest = Contest(
            full_name=full_name,
            roll_no=roll_no,
            section=section,
            shift=shift,
            unique_id=unique_id,
            response=response,
            word_count=word_count
        )
        contest.save()

        flash('Your response has been submitted successfully!', 'success')
        return redirect(url_for('home'))

    flash('Something went wrong!', 'danger')
    return redirect(url_for('home'))


@app.route('/rank')
def rank():
    contest = Contest.select().order_by(Contest.word_count.desc())
    return render_template('rank.html', contest=contest)


if __name__ == '__main__':
    db.connect()
    db.create_tables([Contest])
    app.run(debug=True)
