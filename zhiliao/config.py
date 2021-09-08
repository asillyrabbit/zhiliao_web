import os

PRO_PATH = os.path.dirname(os.path.abspath(__file__))


class RunConfig:
    """
    运行测试配置
    """
    # 运行测试用例的目录或文件
    cases_path = os.path.join(PRO_PATH, "test_dir")

    # 配置浏览器驱动类型(chrome/firefox/chrome-headless/firefox-headless)。
    driver_type = "chrome"

    # 配置运行的 URL
    urls = [
        # 测试-管理后台
        "http://testing.jianyihoutai.xlyhw.com/site/login",
        # 测试-诊室
        "http://zhenshi.testing.xlyhw.com/",
        # 正式-管理后台
        "https://manage.xlyhw.cn/site/login",
        # 诊室-诊室
        "https://zhenshi.xlyhw.cn/user/login"
    ]

    # 失败重跑次数
    rerun = "0"

    # 当达到最大失败数，停止执行
    max_fail = "5"

    # 浏览器驱动（不需要修改）
    driver = None

    # 报告路径（不需要修改）
    NEW_REPORT = None

    # 环境切换标志（0：测试环境 1：正式环境）
    flag = 0

    # 测试医生
    doc_info = [
        {
            # 测试环境
            'mobile': '18684758512',
            'name': '聂军',
            'password': 'Gyy1541%'
        },
        {
            # 正式环境
            'mobile': '18684758512',
            'name': '聂军',
            'password': 'Gyy1541%'
        },
    ]

    # 测试诊所、诊室
    clinic_info = [
        {
            # 测试环境
            'clinic': '自动化测试诊所',
            'room': '第一诊室'
        },
        {
            # 正式环境
            'clinic': '测试诊室二',
            'room': '第一诊室'
        },
    ]

    # 发送邮箱、密码
    from_email = ['niejun@xlyhw.com', 'Gyy2018']

    # 接收邮箱列表
    to_email = ['niejun@xlyhw.com']
