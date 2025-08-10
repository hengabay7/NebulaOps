from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form.get('name', '').strip()
    if name:
        return render_template('greet.html', name=name)
    else:
        return render_template('index.html', error="נא להזין שם")

if __name__ == '__main__':
    app.run(debug=True)
