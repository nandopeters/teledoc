from flask import Flask, request
import twilio.twiml
from twilio.rest import TwilioRestClient
from time import sleep

import helpers

#Twilio
account_sid = "***REMOVED***"
auth_token  = "***REMOVED***"
Tclient = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)

sessions = {}

default_ops = {
  "voice":"woman"
}

@app.route("/", methods=['GET', 'POST'])
def root():
  resp = twilio.twiml.Response()
  resp.say("Hello, welcome to Tele-Doc.",**default_ops)
  resp.say("Please say the country you are in and then press the pound key.", **default_ops)
  resp.record(action="/queue", method="POST", maxLength=7, transcribe=True, transcribeCallback="/transcription-callback")
  return str(resp)

@app.route("/queue", methods=['GET', 'POST'])
def queue():
  resp = twilio.twiml.Response()
  resp.say("Please hold while we look up your location.")
  resp.enqueue("pending") #Put the user in the pending queue.
  return str(resp)

@app.route("/transcription-callback", methods=['GET', 'POST'])
def transcription_cb():
  print "Looking up location"
  location = helpers.get_code_for_country(str(request.values.get('TranscriptionText')))
  call_id = request.values.get('CallSid')
  print request.values.get('TranscriptionText')
  print location
  sessions[call_id] = {
    "location": location,
    "symptom_whitelist": [],
    "symptom_blacklist": []
  }
  member = Tclient.members('***REMOVED***').dequeue("http://teledoc.herokuapp.com/service_select", call_id, method="POST")
  return ""

@app.route("/service_select", methods=['GET', 'POST'])
def service_select():
  resp = twilio.twiml.Response()
  with resp.gather(numDigits=1, action="/service_select_cb", method="POST") as g:
    g.say("If you're in need of immediate medical attention please press 0 to get information about local medical services. Otherwise press 1 to be diagnosed.", **default_ops)
  return str(resp)

@app.route("/service_select_cb", methods=['GET', 'POST'])
def service_select_cb():
  resp = twilio.twiml.Response()
  digit_pressed = request.values.get('Digits', None)
  if digit_pressed == "0": #EMS
    resp.redirect("/ems")
  elif digit_pressed == "1": #Diagnose
    resp.redirect("/diagnose")
  else:
    resp.redirect("/service_select")
  return str(resp)

@app.route("/ems", methods=['GET', 'POST'])
def ems():
  print "Showing number to user"
  number = helpers.get_phone_for_country(sessions[request.values.get('CallSid')]['location'])
  print number
  resp = twilio.twiml.Response()
  resp.say("To get emergency medical attention in your country hang up and dial {0}".format(" ".join(list(str(number)))))
  resp.hangup()
  return str(resp)

###### SMS stuff

# @app.route("/sms", methods=['GET', 'POST'])
# def hello_monkey():

#     body = request.values.get('Body', None)

#     number = helpers.get_phone_for_code(helpers.get_code_for_country(body))
#     message = "Your emergency number is: " + number

#     resp = twilio.twiml.Response()
#     resp.sms(message)

#     return str(resp)

if __name__ == "__main__":
  app.run(debug=True)
