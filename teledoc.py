from flask import Flask, request
import twilio.twiml

app = Flask(__name__)

default_ops = {
  "voice":"women"
}

@app.route("/", methods=['GET', 'POST'])
def root():
  print 'Caller:'
  print request.values.get('From')
  resp = twilio.twiml.Response()
  resp.say("Hello, welcome to teledoc.",**default_ops)
  with resp.gather(numDigits=1, action="/handle-root-key", method="POST") as g:
    g.say("If you're in need of immediate medical attention please press 0 to be connected to local medical services. Otherwise press 2 to be diagnosed.", **default_ops)
  return str(resp)

@app.route("/handle-root-key", methods=['GET', 'POST'])
def handle_root_key():
  digit_pressed = request.values.get('Digits', None)
  if digit_pressed == "0": #EMS
    return redirect("/ems")
  else if digit_pressed == "1": #Diagnose
    return redirect("/diagnose")
  else:
    return redirect("/")

@app.route("/ems", methods=['GET', 'POST'])
def ems():
  resp = twilio.twiml.Response()
  resp.say("We're looking up local EMS services based on your location.",**default_ops)
  return str(resp)

@app.route("/diagnose", methods=['GET', 'POST'])
def diagnose():
  resp = twilio.twiml.Response()
  resp.say("We are diagnosing you.",**default_ops)
  resp.pause(3)
  resp.say("You are going to die.")
  return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
