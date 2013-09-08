from flask import Flask, request
import twilio.twiml
from twilio.rest import TwilioRestClient
from time import sleep
import symptomelimination
import urllib
import redis
import os
import pickle
import helpers

#redis
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)

#Twilio
account_sid = "***REMOVED***"
auth_token  = "***REMOVED***"
Tclient = TwilioRestClient(account_sid, auth_token)

#Session
def set_session(redis, cid, value):
  redis.set(cid, pickle.dumps(value))

def get_session(redis, cid):
  pickled_value = redis.get(cid)
  if pickled_value is None:
    return None
  return pickle.loads(pickled_value)

#App
app = Flask(__name__)

default_ops = {
  "voice":"woman"
}

@app.route("/", methods=['GET', 'POST'])
def root():
  resp = twilio.twiml.Response()
  if get_session(redis, request.values.get('CallSid')) is None:
    resp.say("Hello, welcome to Tele-Doc.",**default_ops)
  resp.say("Please say the country you are in and then press the pound key.", **default_ops)
  resp.record(action="/queue", method="POST", maxLength=7, transcribe=True, transcribeCallback="/transcription-callback")
  return str(resp)

@app.route("/queue", methods=['GET', 'POST'])
def queue():
  resp = twilio.twiml.Response()
  resp.say("Please hold while we look up your location.",**default_ops)
  resp.enqueue("pending") #Put the user in the pending queue.
  return str(resp)

@app.route("/transcription-callback", methods=['GET', 'POST'])
def transcription_cb():
  print "Looking up location"
  location = helpers.get_code_for_country(str(request.values.get('TranscriptionText')))
  call_id = request.values.get('CallSid')
  print request.values.get('TranscriptionText')
  print location
  user_session = {
    "location": location,
    "symptom_whitelist": [],
    "symptom_blacklist": [],
    "question_count": 0
  }
  set_session(redis, call_id, user_session)
  sleep(2)
  member = Tclient.members('***REMOVED***').dequeue("http://teledoc.herokuapp.com/location_check", call_id, method="POST")
  return ""

@app.route("/location_check", methods=['GET', 'POST'])
def location_check():
  resp = twilio.twiml.Response()
  user_session = get_session(redis,request.values.get('CallSid'))
  if not user_session['location']:
    resp.say("We were unabled to look up your location.",**default_ops)
    resp.redirect("/")
    return str(resp)
  location_name = helpers.get_country_for_code(user_session['location'])
  with resp.gather(numDigits=1, action="/location_check_cb", method="POST") as g:
    print location_name
    g.say("You are in {0}. Is that correct? Press 1 for yes, 0 for no.".format(location_name),**default_ops)
  return str(resp)

@app.route("/location_check_cb", methods=['GET', 'POST'])
def location_check_cb():
  resp = twilio.twiml.Response()
  digit_pressed = request.values.get('Digits', None)
  if digit_pressed == "0":
    resp.redirect("/")
  else:
    resp.redirect("/service_select")
  return str(resp)

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
  user_session = get_session(redis,request.values.get('CallSid'))
  number = helpers.get_phone_for_country(user_session['location'])
  print number
  resp = twilio.twiml.Response()
  resp.say("To get emergency medical attention in your country hang up and dial {0}".format(" ".join(list(str(number)))),**default_ops)
  resp.hangup()
  redis.delete(request.values.get('CallSid'))
  return str(resp)

@app.route("/diagnose", methods=['GET', 'POST'])
def diagnose():
  user_session = get_session(redis,request.values.get('CallSid'))
  user_session['question_count']+=1
  set_session(redis, request.values.get('CallSid'), user_session)
  symptoms = symptomelimination.get_ordered_symptom_list(user_session['location'], user_session['symptom_whitelist'], user_session['symptom_blacklist'])
  resp = twilio.twiml.Response()
  print symptoms[0]['symptom']
  with resp.gather(numDigits=1, action="/diagnose_cb?symptom={0}".format(urllib.quote(symptoms[0]['symptom'])), method="POST") as g:
    g.say("Do you have {0}? Press 1 for yes, 0 for no.".format(symptoms[0]['symptom']), **default_ops)
  return str(resp)

@app.route("/diagnose_cb", methods=['GET', 'POST'])
def diagnose_cb():
  user_session = get_session(redis,request.values.get('CallSid'))
  symptom = urllib.unquote(request.args.get('symptom'))
  print symptom
  resp = twilio.twiml.Response()
  digit_pressed = request.values.get('Digits', None)
  if digit_pressed == "1":
    user_session['symptom_whitelist'].append(symptom)
    set_session(redis,request.values.get('CallSid'), user_session)
  else:
    user_session['symptom_blacklist'].append(symptom)
    set_session(redis,request.values.get('CallSid'), user_session)
  diseases = symptomelimination.calculate_probability_for_disease(user_session['location'], user_session['symptom_whitelist'])
  if len(user_session['symptom_whitelist']) == 0:
    for disease in diseases:
      disease['probability'] = 0
  diseases = sorted(diseases, cmp=lambda x, y: cmp(y['probability'],x['probability']))
  for disease in diseases:
    print helpers.get_name_for_disease(disease['disease']), disease['probability']
  if user_session['question_count'] >= 3 and diseases[0]['probability'] > 0.8:
    resp.say("We have determined there is a high probability you have {0}".format(helpers.get_name_for_disease(diseases[0]['disease'])),**default_ops)
    resp.hangup()
    redis.delete(request.values.get('CallSid'))
  elif user_session['question_count'] >= 7:
    resp.say("Sorry, we are unable to determine what you are sick with."**default_ops)
    resp.redirect('/ems')
  else:
    resp.redirect('/diagnose')
  return str(resp)



###### SMS stuff

@app.route("/sms", methods=['GET', 'POST'])
def hello_monkey():
  body = request.values.get('Body', None)
  result = body.replace(' ',',').split(',')
  if( len(result) > 1 ):
    location = helpers.get_code_for_country(result[0])
    symptoms = []
    for i in range(1, len(result)):
      symptoms.append(helpers.get_highst_score_symptom(result[i]))
    symptoms = list(set(symptoms))
    diseases = symptomelimination.calculate_probability_for_disease(location,symptoms)
    message = "We have determined there is a high probability you have {0}".format(helpers.get_name_for_disease(diseases[0]['disease']))
  else:
    number = helpers.get_phone_for_country(helpers.get_code_for_country(body))
    message = "Your emergency number is: " + number
  resp = twilio.twiml.Response()
  resp.sms(message)
  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)
