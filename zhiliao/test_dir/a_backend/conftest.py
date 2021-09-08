import pytest
from zhiliao.config import RunConfig

# 登录用户名/密码
b_account = [
    {
        'username': 'admin',
        'password': '123456'
    },
    {
        'username': 'niejun',
        'password': 'Shengjiang@1541%'
    }
]


# 管理后台登录用户名/密码
@pytest.fixture(scope='function')
def back_account():
    if RunConfig.flag == 0:
        return b_account[0]
    else:
        return b_account[1]
