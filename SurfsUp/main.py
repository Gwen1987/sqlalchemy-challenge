from flask import Flask



app = Flask(__name__)

print(app)
@app.route('/')
def index():
  return 'index'

@app.route('/api/v1.0/precipitation')
def foo():
  return 'hello there'



app.run(debug=False)
with app.test_client() as client:
  response = client.get('/api/v1.0/precipitation')
  print(response.status_code)
