from celery import shared_task


@shared_task
def flowable_task_demo():
    print(1)
