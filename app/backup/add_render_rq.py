#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs

 
from redis import Redis
import rq

queue = rq.Queue('menta4-tasks', connection=Redis.from_url('redis://'))
job = queue.enqueue('app.tasks.render_std_dsts_with_rq', 23)
job.get_id()
'c651de7f-21a8-4068-afd5-8b982a6f6d32'