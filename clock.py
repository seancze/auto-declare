from apscheduler.schedulers.blocking import BlockingScheduler
from main import declare

sched = BlockingScheduler()

# start_time = time.time()

# Run morning tasks - Weekly Declaration (Runs between 07:28 and 09:28 every Monday)
sched.add_job(declare, 'cron', day_of_week=0, hour=8, minute=28, jitter=3600, misfire_grace_time=None, timezone="Canada/Eastern")
# sched.add_job(declare, 'cron', day_of_week=2, hour=14, minute=44, misfire_grace_time=None, timezone="Canada/Eastern")

sched.start()
