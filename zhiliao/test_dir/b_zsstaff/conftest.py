from zhiliao.config import RunConfig
import pytest
import random
import time

# Start------>员工端登录：账号/密码 ------
# 登录用户名/密码
s_account = [
    {
        'username': 'shengjiang3',
        'password': '123456'
    },
    {
        'username': 'shengjiang',
        'password': '123456'
    }
]


# 员工端登录用户名/密码
@pytest.fixture(scope='function')
def staff_account():
    if RunConfig.flag == 0:
        return s_account[0]
    else:
        return s_account[1]


# End------>员工端登录：账号/密码 ------


# Start------>挂号登记：患者信息、挂号信息 ------
# 按日期生成一个新号码
def random_mobile():
    cur_day = time.strftime('%m%d', time.localtime())
    mobile = f'190{cur_day}0000'

    return mobile


def random_name():
    baijiaxing = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    shuzi = '一二三五六七八九十'
    xing = baijiaxing[random.randint(0, len(baijiaxing) - 1)]
    ming = shuzi[random.randint(0, len(shuzi) - 1)]
    name = f'测试{xing}{ming}'

    return name


# 患者信息
pat_info = [
    {
        'title': '新号+新患者+身份证+男+异常',
        'p_type': 'new',
        'mobile': random_mobile(),
        'name': random_name(),
        'gender': '男',
        'birthday': '1990-06-06',
        'id_card': '110101199006065656'
    },
    {
        'title': '老号+新患者+非身份证+女',
        'p_type': 'new',
        'mobile': random_mobile(),
        'name': random_name(),
        'gender': '女',
        'birthday': '1990-06-06',
        'id_card': 'TEST19900606'
    },
    {
        'title': '老号+老患者+身份证+男',
        'p_type': 'old',
        'mobile': 18684758512,
        'name': '生姜',
        'gender': '男',
        'birthday': '1996-06-06',
        'id_card': '110101199606069108'
    }
]

# End------>挂号登记：患者信息、挂号信息 ------
