import os
import sys
import time
import json
import logging
import logging.handlers
from subprocess import call

import yaml
from TwitterAPI import TwitterAPI, TwitterRequestError, TwitterConnectionError

logger = logging.getLogger(__name__)
handler = logging.handlers.SysLogHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

def setLed(color):
  call([ 'expled', color ])
  return

def setPin(value):
  call([ 'ubus', 'call', 'gpio', 'set_pin', json.dumps({ 'pin': 0, 'value': value }) ])
  return

logger.info('Initializing')

setLed('0000ff')

configStream = open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r')
config = yaml.load(configStream)
configStream.close()

api = TwitterAPI(
  config['twitter']['consumerKey'],
  config['twitter']['consumerSecret'],
  config['twitter']['accessTokenKey'],
  config['twitter']['accessTokenSecret']
)

while True:
  try:
    logger.info('Requesting');
    iterator = api.request('user').get_iterator()

    setLed('00ff00')

    for item in iterator:
      if 'text' in item:
        if item['user']['screen_name'] == 'DoorbellNudger':
          logger.info(unicode(item['text']))

          if '#ringit' in item['text']:
            logger.info("Ringing it!")
            setPin(1);
            setLed('ff00ff')
            time.sleep(1)
            setPin(0);
            setLed('00ff00')
      elif 'disconnect' in item:
        event = item['disconnect']

        if event['code'] in [ 2, 5, 6, 7 ]:
          # something needs to be fixed before re-connecting
          setLed('ff0000')
          logger.error(event['reason'])
          raise Exception(event['reason'])
        else:
          # temporary interruption, re-try request
          logger.warning('Disconnected, retrying');
          time.sleep(5)
          break
  except TwitterRequestError as e:
    if e.status_code < 500:
      # something needs to be fixed before re-connecting
      setLed('ff0000')
      logger.error(e.status_code)
      raise
    else:
      # temporary interruption, re-try request
      logger.warning('Request error, retrying');
      time.sleep(5)
      pass
  except TwitterConnectionError:
    # temporary interruption, re-try request
    logger.warning('Connection error, retrying');
    time.sleep(5)
    pass
