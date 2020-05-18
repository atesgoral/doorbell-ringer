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

# def call(args):
#   logger.info('Stub call: %s', args)
#   return

def flashLed(r, g, b):
  call([ 'fast-gpio', 'set', '17', str(1 - r) ])
  call([ 'fast-gpio', 'set', '16', str(1 - g) ])
  call([ 'fast-gpio', 'set', '15', str(1 - b) ])
  call([ 'fast-gpio', 'set', '17', '1' ])
  call([ 'fast-gpio', 'set', '16', '1' ])
  call([ 'fast-gpio', 'set', '15', '1' ])
  return

def setButton(value):
  call([ 'relay-exp', '-i', '0', str(value) ])
  return

def setText(text):
  call([ 'oled-exp', '-i', '-c', '-q', 'write', text ])
  return

logger.info('Initializing')
setText('Initializing')

flashLed(0, 0, 1)

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
    logger.info('Streaming tweets')
    setText('Streaming tweets')
    iterator = api.request('statuses/filter', { 'follow': '712819138490671104' }).get_iterator()

    flashLed(0, 1, 0)

    for item in iterator:
      if 'text' in item:
        if item['user']['screen_name'] == 'DoorbellNudger':
          logger.info(unicode(item['text']))

          if '#ringit' in item['text']:
            api.request('statuses/update', { 'status': '@DoorbellNudger OK! Ringing it!', 'in_reply_to_status_id': item['id'] });

            logger.info('Ringing it!')
            setText('Ringing it!')

            flashLed(1, 0, 1)
            setButton(1);

            time.sleep(1)

            logger.info('Waiting')
            setText('Waiting')

            setButton(0)
          elif '#update' in item['text']:
            api.request('statuses/update', { 'status': '@DoorbellNudger OK! Self-updating. See you in a bit...', 'in_reply_to_status_id': item['id'] });

            logger.info('Updating!')
            setText('Updating!')

            flashLed(1, 1, 0)

            call([ '/etc/init.d/doorbell-ringer', 'update' ])
            call([ '/etc/init.d/doorbell-ringer', 'restart' ])
      elif 'disconnect' in item:
        event = item['disconnect']

        if event['code'] in [ 2, 5, 6, 7 ]:
          # something needs to be fixed before re-connecting
          flashLed(1, 0, 0)
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
      flashLed(1, 0, 0)
      logger.error(e.status_code)
      setText('Waiting 10s')
      time.sleep(10)
      pass
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
