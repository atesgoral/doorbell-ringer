import os
import sys
import time
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

def setPin(pin, value):
  call([ 'ubus', 'call', 'gpio', 'set_pin', '{"pin":{0},"value":{1}}'.format(pin, value) ])
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
          logger.info("%s\n" % unicode(item['text']))

          if '#ringit' in item['text']:
            logger.info("Ringing it!\n")
            setPin(0, 1);
            setLed('ff00ff')
            time.sleep(1)
            setPin(0, 0);
            setLed('00ff00')
      elif 'disconnect' in item:
        event = item['disconnect']

        if event['code'] in [ 2, 5, 6, 7 ]:
          # something needs to be fixed before re-connecting
          setLed('ff0000')
          raise Exception(event['reason'])
        else:
          # temporary interruption, re-try request
          logger.info('Disconnected, retrying');
          break
  except TwitterRequestError as e:
    if e.status_code < 500:
      # something needs to be fixed before re-connecting
      setLed('ff0000')
      raise
    else:
      # temporary interruption, re-try request
      logger.info('Request error, retrying');
      pass
  except TwitterConnectionError:
    # temporary interruption, re-try request
    logger.info('Connection error, retrying');
    pass
