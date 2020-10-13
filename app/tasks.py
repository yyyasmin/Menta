#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs

import time
from rq import get_current_job

from app import create_app

app = create_app()
app.app_context().push()


def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')
    

#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs
@std.route('/render_std_dsts_with_rq', methods=['GET', 'POST'])
@login_required
def render_std_dsts_with_rq(  std, student_dsts, dsts_not_of_student,  \
                            all_goals, student_goals, goals_not_of_student,  \
                            all_todos, student_todos, todos_not_of_student,  \
                            std_txts,  \
                            statuss, default_status,  \
                            whos, default_who,  \
                            tags, age_ranges,  \
                            due_date):

    try:
    
        _set_task_progress(0)
        i=0
        
        t = render_template('./destinations/table_destinations/edit_all_dsts.html', std=std,  
                                                        student_dsts=student_dsts, dsts_not_of_student=dsts_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date)

    i += 1
    _set_task_progress(100 * i // student_dsts.count())

    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        

### Job progress notification to user 
def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()
        
        

#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs
@std.route('/student_dsts', methods=['GET', 'POST'])
@login_required
def student_dsts(  std, student_dsts, dsts_not_of_student,  \
                            all_goals, student_goals, goals_not_of_student,  \
                            all_todos, student_todos, todos_not_of_student,  \
                            std_txts,  \
                            statuss, default_status,  \
                            whos, default_who,  \
                            tags, age_ranges,  \
                            due_date):

    try:
    
        _set_task_progress(0)
        i=0
        
        t = render_template('./destinations/table_destinations/edit_all_dsts.html', std=std,  
                                                        student_dsts=student_dsts, dsts_not_of_student=dsts_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date)

    i += 1
    _set_task_progress(100 * i // student_dsts.count())

    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        
