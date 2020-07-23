

from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 201

    # 小程序登陆
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201