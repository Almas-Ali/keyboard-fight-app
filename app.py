from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Contest, Timer
import datetime

app = Flask(__name__)
app.secret_key = b'secret-this-is-a-secret-key-24525-235-%^$%_@#%@_535NNVUbbijw_jigr'


@app.route('/')
def home():
    # Get the latest timer
    timer = Timer.select().order_by(Timer.id.desc()).first().get_time()
    return render_template('index.html', timer=timer)


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        full_name: str = request.form['full_name']
        roll_no: int = int(request.form['roll'])
        section: str = request.form['section']
        shift: str = request.form['shift']

        response: str = request.form['response']

        word_count: int = len(response.split(' '))

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


@app.route('/set-time', methods=['POST', 'GET'])
def set_timer():
    if request.method == 'POST':
        selected_time = request.form['time']

        _timer = Timer(
            selected_time=selected_time,
            timestamp=datetime.datetime.now()
        )
        _timer.save()

        flash('Timer has been set successfully!', 'success')
        return redirect(url_for('home'))

    flash('Something went wrong!', 'danger')
    return redirect(url_for('home'))


if __name__ == '__main__':
    db.connect()
    db.create_tables([Contest, Timer])
    app.run(host='0.0.0.0', port=5000, debug=True)
