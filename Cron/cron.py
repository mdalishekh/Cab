from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from Configuration.config import *
import time

# This will print a log in server side 
def cron_job():
    logging.info("---------------------------------------------------------")
    logging.info(f"KEEPING SERVER ACTIVE IN EVERY MINUTE {datetime.now().strftime('%Y-%m-%d at %H-%M-%S')}")
    logging.info("---------------------------------------------------------")

# This function in controlling Crin expression
def cron_scheduler():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(minute='*', hour='*', day='*', month='*', day_of_week='*')
    scheduler.add_job(lambda: cron_job(), trigger)
    scheduler.start()
    try:
        while scheduler.running:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)