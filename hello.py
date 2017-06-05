from flask import Flask, render_template
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    title = "toppage"
    message = "input your name"
    return render_template("index.html", message=message, title=title)
    #return 'Hello World!'

if __name__ == '__main__':
    app.run()

