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
        "",
        # 测试-诊室
        ""
    ]

    # 失败重跑次数
    rerun = "0"

    # 当达到最大失败数，停止执行
    max_fail = "5"

    # 浏览器驱动（不需要修改）
    driver = None

    # 报告路径（不需要修改）
    NEW_REPORT = None

    # 测试医生
    doc_info = {
        'mobile': '',
        'name': '',
        'password': ''
    }

    # 测试诊所、诊室
    clinic_info = {
        'clinic': '自动化测试诊所',
        'room': '第一诊室'
    }
