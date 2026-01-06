from celery import shared_task


@shared_task
def user_task_demo():
    print(1)
