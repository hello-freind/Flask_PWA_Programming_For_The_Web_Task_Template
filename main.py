from flask import Flask
from flask import render_template
from flask import request
import database_manager as dbHandler

app = Flask(__name__)

@app.route('/homepagep.html', methods=['GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
  return render_template('/homepage.html')

@app.route('/add.html', methods=['GET'])
def add():
  return render_template('/add.html')  

@app.route('/about.html', methods=['GET'])
def about():
  return render_template('/about.html')

@app.route('/otherpage.html', methods=['GET'])
def otherpage():
  return render_template('/otherpage.html')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5100)


