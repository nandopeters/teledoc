from flask import Flask, request
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
  """Respond to incoming requests."""

  print 'Caller:'
  print request.values.get('From')

  resp = twilio.twiml.Response()
  resp.say("Hello Monkey")

  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)
