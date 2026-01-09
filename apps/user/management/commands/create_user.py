import ast

from django.core.management import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = '创建新用户'
    """
        python manage.py create_user '{"username":"admin","name":"admin","password":"admin"}'
    """
    def add_arguments(self, parser):
        parser.add_argument("user_data", help="用户数据字典")

    def handle(self, *args, **options):
        user_data = options['user_data']
        data = ast.literal_eval(user_data)
        if not isinstance(data, dict):
            raise ValueError(f"{user_data} 无法转换成字典数据")

        other = {"username", "name", "password"} - set(list(data.keys()))
        if other:
            raise ValueError(f"必须包含 {other}字段")

        if User.objects.filter(username=data.get("username")).exists():
            print("用户已经存在")

        User.objects.create(username=data.get("username"),
                            name=data.get("name"),
                            password=data.get("password"))
