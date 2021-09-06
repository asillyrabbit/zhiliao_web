import pytest

# 登录用户名/密码
b_account = {
    'username': '',
    'password': ''
}


# 管理后台登录用户名/密码
@pytest.fixture(scope='function')
def back_account():
    return b_account
