from cryptography.fernet import Fernet

from pyflowable import settings


class Signer:
    """
    用来加密,解密,和基于时间戳的方式验证token
    """

    def __init__(self, key=None):
        """
            初始化
        :param key: 盐
        """
        self.fnt = Fernet(key)

    @staticmethod
    def make_key():
        """
            生成一个随机字符串
        """
        return Fernet.generate_key().decode("utf-8")

    def encrypt(self, dat):
        """
        加密
        :param dat: bytes or string
        :return: string
        """
        if isinstance(dat, str):
            dat = dat.encode('utf-8')
        assert isinstance(dat, bytes), 'The argument `dat` must be a bytes or a string.'
        return self.fnt.encrypt(dat).decode('utf-8')

    def decrypt(self, dat):
        """
        解密
        若dat非encrypt加密的数据，会抛出异常：
            cryptography.fernet.InvalidToken
        :param dat: bytes or string
        :return: string
        """
        if isinstance(dat, str):
            dat = dat.encode('utf-8')
        assert isinstance(dat, bytes), 'The argument `dat` must be a bytes or a string.'
        return self.fnt.decrypt(dat).decode('utf-8')


signer = Signer(settings.SECRET_KEY)