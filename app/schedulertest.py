from flask_apscheduler import APScheduler
from app import app


scheduler = APScheduler()

scheduler.init_app(app)

@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def job1():
    print('Job 1 executed')
# scheduler.add_job(
#     id='print_hello_world',
#     func=printMessage,
#     args=('hello from the scheduler!',),
#     trigger='interval',
#     seconds=3
# )
scheduler.start()