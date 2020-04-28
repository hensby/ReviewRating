from flask import Flask, url_for, request, redirect, Blueprint
from flask import render_template
import model

app = Flask(__name__)

bp = Blueprint('task_list', __name__)
# @app.route('/')
@app.route('/')
def hello():
    return render_template('review.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        lr_y_predict, svm_y_predict, random_forest_y_predict, bayes_y_predict = model.predict(request.form['review'])
        result = {'linear regression score': lr_y_predict,
                  'svm score': svm_y_predict,
                  'random_forest': random_forest_y_predict,
                  'bayes linear regression score': bayes_y_predict}
        return render_template("result.html", result=result)


if __name__ == '__main__':
    app.run()
