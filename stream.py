import yaml
import sys
import codecs

from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterRequestError
from TwitterAPI import TwitterConnectionError


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

#r = api.request('user')

#for item in r:
#  print(item)

while True:
  try:
    iterator = api.request('statuses/filter', {'track':'pizza'}).get_iterator()
    for item in iterator:
      if 'text' in item:
        out.write("%s\n" % item['text'])
        #print(item['text'])
      elif 'disconnect' in item:
        event = item['disconnect']
        if event['code'] in [2,5,6,7]:
          # something needs to be fixed before re-connecting
          raise Exception(event['reason'])
        else:
          # temporary interruption, re-try request
          break
  except TwitterRequestError as e:
    if e.status_code < 500:
      # something needs to be fixed before re-connecting
      raise
    else:
      # temporary interruption, re-try request
      pass
  except TwitterConnectionError:
    # temporary interruption, re-try request
    pass
