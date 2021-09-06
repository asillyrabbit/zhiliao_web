from poium import Page, Element, Elements


class StaffPage(Page):
    # 登录页
    login_id = Element(id_='staffLogin', describe='员工登录')
    username = Element(id_='username', describe='用户名')
    password = Element(id_='password', describe='密码')
    login_btn = Element(id_='clinicLogin', describe='登录按钮')
    register_menu = Element(xpath='//*[@id="registe"]/a', describe='挂号登记菜单')

    # 挂号页
    st_frame = Element(id_='workspace', describe='挂号登记页iframe')
    patient_register = Element(link_text="登记", describe='挂号页登记按钮')
    patient_mobile = Element(id_='mobile', describe='患者手机号')
    first_patient = Element(xpath='//*[@id="patientList"]/a[1]')
    patient_name = Element(id_='patientName', describe='患者姓名')
    birthday = Element(id_='birthday', describe='生日')
    id_card = Element(id_='idCard', describe='身份证')
    jz_time_div = Element(id_='smallTimeDiv', describe='就诊时段div')
    jz_times = Elements(xpath='//*[@id="smallTimeDiv"]/div/a', describe='所有就诊时段')
    re_submit = Element(id_='submit', describe='挂号登记提交')

    # 收费页
    pay_types = Elements(xpath='//*[@id="payType"]/a', describe='支付方式数组')
    pay_input = Element(xpath='//*[@id="feeWindow"]/div[2]/div[2]/div/div[4]/div[2]/input', describe='企业支付第三方名称')
    fee_confirm = Element(id_='feeConfirm', describe='收费页确认按钮')
    fee_confirm_submit = Element(id_='feeConfirmSubmit', describe='确认并打印挂号条')

    # 挂号列表页
    result = Element(xpath='//tbody/tr[2]/td[11]/a[1]', describe='挂号列表页第一行中的已到店标识')

    # 退出登录
    login_name = Element(xpath='//*[@id="main_admin_top_name"]/span', describe='当前登录用户')
    logout = Element(xpath='//div/div[1]/div/div[4]/a[2]', describe='退出系统')
