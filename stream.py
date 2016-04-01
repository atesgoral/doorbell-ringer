import os
import sys
import codecs
import time
from subprocess import call

import yaml
from TwitterAPI import TwitterAPI, TwitterRequestError, TwitterConnectionError

call([ 'expled', '0000ff' ])

configStream = open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r')
config = yaml.load(configStream)
configStream.close()

out = codecs.getwriter('utf-8')(sys.stdout)

api = TwitterAPI(
  config['twitter']['consumerKey'],
  config['twitter']['consumerSecret'],
  config['twitter']['accessTokenKey'],
  config['twitter']['accessTokenSecret']
)

while True:
  try:
    print('Requesting');
    iterator = api.request('user').get_iterator()

    call([ 'expled', '00ff00' ])

    for item in iterator:
      if 'text' in item:
        if item['user']['screen_name'] == 'DoorbellNudger':
          out.write("%s\n" % item['text'])

          if '#ringit' in item['text']:
            out.write("Ringing it!\n")
            call([ 'ubus', 'call', 'gpio', 'set_pin', '{"pin":0,"value":1}' ])
            call([ 'expled', 'ff00ff' ])
            time.sleep(1)
            call([ 'ubus', 'call', 'gpio', 'set_pin', '{"pin":0,"value":0}' ])
            call([ 'expled', '00ff00' ])
      elif 'disconnect' in item:
        event = item['disconnect']

        if event['code'] in [ 2, 5, 6, 7 ]:
          # something needs to be fixed before re-connecting
          call([ 'expled', 'ff0000' ])
          raise Exception(event['reason'])
        else:
          # temporary interruption, re-try request
          print('Disconnected, retrying');
          break
  except TwitterRequestError as e:
    if e.status_code < 500:
      # something needs to be fixed before re-connecting
      call([ 'expled', 'ff0000' ])
      raise
    else:
      # temporary interruption, re-try request
      print('Request error, retrying');
      pass
  except TwitterConnectionError:
    # temporary interruption, re-try request
    print('Connection error, retrying');
    pass
