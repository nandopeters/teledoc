import subprocess
import json

def call_att_api(audiofile, grammarfile):
  print ['curl', "-s", "https://api.att.com/speech/v3/speechToTextCustom", '--insecure', '--request', 'POST', '--header', "Authorization: Bearer RcYUPOu1wCeZ5YXcnUY0FI3B2t3B0Qmn", '--header', "Content-type: multipart/x-srgs-audio", '--header', "Accept: application/json", '--header', "X-SpeechContext: GrammarList", '--form', "x-grammar=@" + grammarfile + ";type=application/srgs+xml", '--form', "x-voice=@" + audiofile + "; type=audio/wav"]
  response = json.loads(subprocess.check_output(['curl', "-s", "https://api.att.com/speech/v3/speechToTextCustom", '--insecure', '--request', 'POST', '--header', "Authorization: Bearer RcYUPOu1wCeZ5YXcnUY0FI3B2t3B0Qmn", '--header', "Content-type: multipart/x-srgs-audio", '--header', "Accept: application/json", '--header', "X-SpeechContext: GrammarList", '--form', "x-grammar=@" + grammarfile + ";type=application/srgs+xml", '--form', "x-voice=@" + audiofile + "; type=audio/wav"]))
  return response['Recognition']['NBest'][0]['ResultText']

if __name__ == '__main__':
  print call_att_api('/Users/tobias/Desktop/rec.wav', '/Users/tobias/Desktop/country_grammar.xml')
