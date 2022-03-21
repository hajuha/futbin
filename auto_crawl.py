from main import SoccerGuru
import schedule
import os
import time
from decouple import config

PICKLE_FILE_NAME = config('PICKLE_FILE_NAME')
DRAFT_PICKLE_FILE_NAME = config('DRAFT_PICKLE_FILE_NAME')

def crawl():
    a = SoccerGuru()
    a.create_pickle()
    
    try:
        os.remove(PICKLE_FILE_NAME)
    except:
        print("Error while deleting file ", PICKLE_FILE_NAME)
        
    os.rename(DRAFT_PICKLE_FILE_NAME, PICKLE_FILE_NAME)
    
# crawl()
schedule.every(60).minutes.do(crawl)

def run():
    while 1:
        schedule.run_pending()
        time.sleep(1)

