from flask import Flask
from flask import render_template
from flask import request
import database_manager as dbHandler

app = Flask(__name__)

@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
  return render_template('/index.html')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5100)


@app.route('/newpage')
def new_page():
  return render_template('homepage.html')

