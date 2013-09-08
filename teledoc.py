from flask import Flask, request
import twilio.twiml

import helpers

app = Flask(__name__)

default_ops = {
  "voice":"woman"
}

@app.route("/", methods=['GET', 'POST'])
def root():
  resp = twilio.twiml.Response()
  resp.say("Hello, welcome to teledoc.",**default_ops)
  with resp.gather(numDigits=1, action="/handle-root-key", method="POST") as g:
    g.say("If you're in need of immediate medical attention please press 0 to be connected to local medical services. Otherwise press 1 to be diagnosed.",**default_ops)
  return str(resp)

@app.route("/handle-root-key", methods=['GET', 'POST'])
def handle_root_key():
  resp = twilio.twiml.Response()
  digit_pressed = request.values.get('Digits', None)
  if digit_pressed == "0": #EMS
    resp.redirect("/ems")
  elif digit_pressed == "1": #Diagnose
    resp.redirect("/diagnose")
  else:
    resp.redirect("/")
  return str(resp)

@app.route("/ems", methods=['GET', 'POST'])
def ems():
  resp = twilio.twiml.Response()
  resp.say("Please say the country you are in and then press the pound key.", **default_ops)
  resp.record(action="/ems-country", method="POST", maxLength=30, transcribe=True, transcribeCallback="/ems-country-transcription")
  phonecountry = request.values.get('FromCountry')
  return str(resp)

@app.route("/ems-country", methods=['GET', 'POST'])
def ems_country():
  resp = twilio.twiml.Response()
  resp.hangup()
  return str(resp)

@app.route("/ems-country-transcription", methods=['GET', 'POST'])
def ems_country_transcription():
  print request.values.get('TranscriptionStatus'), request.values.get('TranscriptionText')
  print "Looking up the phone number"
  print helpers.get_phone_for_code(helpers.get_code_for_country(str(request.values.get('TranscriptionText'))))
  return ""

@app.route("/diagnose", methods=['GET', 'POST'])
def diagnose():
  resp = twilio.twiml.Response()
  resp.say("We are diagnosing you.",**default_ops)
  resp.pause(length=3)
  resp.say("You are going to die.",**default_ops)
  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)
