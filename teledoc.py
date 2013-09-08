from flask import Flask, request
import twilio.twiml
from twilio.rest import TwilioRestClient

import helpers

#Twilio
account_sid = "***REMOVED***"
auth_token  = "***REMOVED***"
Tclient = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)

default_ops = {
  "voice":"woman"
}

@app.route("/", methods=['GET', 'POST'])
def root():
  resp = twilio.twiml.Response()
  resp.say("Hello, welcome to Tele-Doc.",**default_ops)
  with resp.gather(numDigits=1, action="/handle-root-key", method="POST") as g:
    g.say("If you're in need of immediate medical attention please press 0 to be connected to local medical services. Otherwise press 1 to be diagnosed.", **default_ops)
  return str(resp)

@app.route("/handle-root-key", methods=['GET', 'POST'])
def handle_root_key():
  resp = twilio.twiml.Response()
  digit_pressed = request.values.get('Digits', None)
  if digit_pressed == "0": #EMS
    resp.redirect("/ems-record")
  elif digit_pressed == "1": #Diagnose
    resp.redirect("/diagnose")
  else:
    resp.redirect("/")
  return str(resp)

@app.route("/ems-record", methods=['GET', 'POST'])
def ems():
  resp = twilio.twiml.Response()
  resp.say("Please say the country you are in and then press the pound key.", **default_ops)
  resp.record(action="/ems-queue", method="POST", maxLength=30, transcribe=True, transcribeCallback="/ems-transcription-callback?call_id={0}".format(request.values.get('CallSid')))
  return str(resp)

@app.route("/ems-queue", methods=['GET', 'POST'])
def ems_queue():
  resp = twilio.twiml.Response()
  resp.say("Please hold while we look up the local E M S services.")
  resp.enqueue("pending") #Put the user in the pending queue.
  return str(resp)

@app.route("/ems-transcription-callback", methods=['GET', 'POST'])
def ems_country_transcription():
  print "Looking up the phone number"
  number = helpers.get_phone_for_code(helpers.get_code_for_country(str(request.values.get('TranscriptionText'))))
  call_id = request.values.get('CallSid')
  print request.values.get('TranscriptionStatus'), request.values.get('TranscriptionText')
  print number
  print call_id
  Tclient.members('***REMOVED***').dequeue("http://teledoc.herokuapp.com/ems-finish?ems_number={0}".format(number),call_id, method="POST")
  return ""

@app.route("/ems-finish", methods=['GET', 'POST'])
def ems_finish():
  number = request.args.get('ems_number')
  print "Showing number to user"
  print number
  resp = twilio.twiml.Response()
  resp.say("To get emergency medical attention in your country hang up and dial {0}".format(number))
  resp.hangup()
  return str(resp)

@app.route("/diagnose", methods=['GET', 'POST'])
def diagnose():
  resp = twilio.twiml.Response()
  resp.say("We are diagnosing you.",**default_ops)
  resp.pause(length=3)
  resp.say("You are going to die.",**default_ops)
  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)
