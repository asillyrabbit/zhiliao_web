from poium import Page, Element, Elements


class BackendPage(Page):
    # 登录页面
    user_name = Element(id_="loginform-username", describe="登录名")
    pass_word = Element(id_="loginform-password", describe="密码")
    captcha = Element(id_="loginform-captcha", describe="验证码")
    captcha_image = Element(id_="loginform-captcha-image", describe="验证码图片标签")
    login_button = Element(name="login-button", describe="登录")

    # 知了诊室
    zl_zhenshi = Element(link_text="知了诊室", describe="左侧导航栏菜单")
    chuzhe_doc = Element(xpath='//*[@id="side-menu"]/li[10]/ul/li[4]/a', describe="出诊医生")
    zs_iframes = Elements(tag="iframe", describe="当前所有iframe")
    yy_doc_moblie = Element(xpath='//form/div/div[1]/div[5]/div/input', describe="医生手机号")
    zs_sh_button = Element(xpath='//form/div/div[2]/div/button', describe="搜索按钮")
    yy_count = Elements(xpath='//tbody/tr/td', describe="预约记录数")
    add_scheduling = Element(link_text="添加排班", describe="添加排班")
    scheduling_day = Element(id_="consultingroomscheduling-day", describe="排班日期")
    yy_doc = Element(id_='consultingroomscheduling-doctor_name', describe="排班医生")
    temp_name = Element(id_="temp_name", describe="符合查询条件的医生")
    submits = Element(id_="submits", describe="提交按钮")

    # 退出系统
    logout = Element(class_name='J_tabExit', describe='退出系统')
