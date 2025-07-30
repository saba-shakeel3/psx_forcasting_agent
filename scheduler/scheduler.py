# scheduler/scheduler_aps.py
from apscheduler.schedulers.blocking import BlockingScheduler
import os

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def scheduled_job():
    print("Running scheduled pipeline...")
    os.system("python main.py")
    print("Pipeline run complete.")

sched.start()
