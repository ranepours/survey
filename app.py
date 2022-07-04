from flask import Flask, render_template, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = 'responses'

@app.route('/')
def show_home():
    """choose survey"""
    return render_template('base.html', survey=survey)

@app.route('/begin', methods=["POST"])
def begin_survey():
    """survey start"""
    session[responses] = []
    return redirect('/questions/0')

@app.route('/questions/<int:id>')
def show_question(id):
    """display q"""
    res = session.get(responses)
    if(res is None):
        return redirect('/')
    if(len(res) == len(survey.questions)):
        return redirect('/complete')
    if(len(res) != id):
        flash(f"Invalid question id: {id}")
        return redirect(f"/questions/{len(res)}")

    question = survey.questions[id]
    return render_template('question.html', question_num=id, question=question)

@app.route('/answer', methods=['POST'])
def handle_question():
    """save answer, next question"""
    answered = request.form['answer'] #grab response
    res = session[responses] #add to list
    res.append(answered)
    session[responses] = res

    if(len(res) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(res)}")

@app.route('/complete')
def done():
    """survey finished"""
    return render_template('complete.html')