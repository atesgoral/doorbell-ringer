import sys
import codecs
import time

import yaml
from TwitterAPI import TwitterAPI, TwitterRequestError, TwitterConnectionError

configStream = open('config.yml', 'r')
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
    print('requesting');
    iterator = api.request('user').get_iterator()

    for item in iterator:
      if 'text' in item:
        if item['user']['screen_name'] == 'DoorbellNudger':
          out.write("%s\n" % item['text'])

          if '#ring-it' in item['text']:
            out.write("Ringing it!\n")
            time.sleep(1)
      elif 'disconnect' in item:
        event = item['disconnect']

        if event['code'] in [ 2, 5, 6, 7 ]:
          # something needs to be fixed before re-connecting
          raise Exception(event['reason'])
        else:
          # temporary interruption, re-try request
          print('disconnected, retrying');
          break
  except TwitterRequestError as e:
    if e.status_code < 500:
      # something needs to be fixed before re-connecting
      raise
    else:
      # temporary interruption, re-try request
      print('request error, retrying');
      pass
  except TwitterConnectionError:
    # temporary interruption, re-try request
    print('connection error, retrying');
    pass
