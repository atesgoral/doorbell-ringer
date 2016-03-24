import yaml
import sys
import codecs

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

#r = api.request('user')

#for item in r:
#  print(item)

rateLimitStatus = api.request('application/rate_limit_status');
mentions = rateLimitStatus.json()['resources']['statuses']['/statuses/mentions_timeline'];

if mentions['remaining'] == 0:
  print('Rate limit exceeded');
  # reset, limit
  sys.exit()

while True:
  try:
    print('requesting');
    iterator = api.request('statuses/mentions_timeline', {
      #'count': 1,
      #'include_rts': 1,
      #'include_entities': 0
    }).get_iterator()

    for item in iterator:
      if 'text' in item:
        out.write("%s\n" % item['text'])
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
