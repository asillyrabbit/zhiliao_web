from poium import Page, Element, Elements


class DoctorPage(Page):
    # 登录页
    login_doctor_pwd = Element(id_='login_doctor_pwd', describe='密码登录方式')
    doctor_mobile = Element(id_='doctor_mobile', describe='医生手机号')
    doctor_password = Element(id_='doctor_password', describe='医生密码')
    clinic_login = Element(id_='clinicLogin', describe='诊室登录按钮')
    select_clinic_determine = Element(id_='select_clinic_determine', describe='选择诊所弹窗页确认按钮')
    pat_menu = Element(id_='patient', describe='门诊诊室菜单')

    # 接诊页
    frame = Element(id_='workspace', describe='接诊页iframe')
    first_row = Element(xpath='//table/tbody/tr[2]/td[14]/a', describe='待接诊列表第一行')
    jz_confirm = Element(xpath='//*[@id="window"]/div[2]/div[3]/div[2]/a', describe='接诊弹窗确认')
    created_prescription = Element(link_text='prescription', describe='已开处方菜单')
    jz_rows = Elements(xpath='//*[@id="app222"]/table/tbody/tr/td[14]/a', describe='接诊列表所有记录')

    # 开方页
    diagnosis = Element(id_='diagnosis', describe='诊断')
    dialectical = Element(id_='dialectical', describe='辨证')
    complaint = Element(id_='complaint', describe='主诉')
    allergy = Element(id_='allergy', describe='过敏史')
    medicine = Element(id_='medicine', describe='同期服用药物')

    drug_selects = Elements(xpath='//*[@class="reception_basic_topinforbox"]/div[1]/div[2]/select', describe='剂型选择下拉框')
    change_confirm = Element(xpath='//*[@id="content"]/div[3]/div[2]/div[3]/div[2]/a', describe='变更剂型确定按钮')
    sup_selects = Elements(xpath='//*[@class="form_select supplierSelect"]', describe='药房选择下拉框')
    sup_sel_opts = Elements(xpath='//*[@class="form_select supplierSelect"]/option', describe='药房选择下拉框选项')

    input_drug_names = Elements(xpath='//*[@class="edit_input_box addDrug"]/div/div[1]/input', describe='药品输入框')
    sel_drugs = Elements(xpath='//*[@class="edit_input_box addDrug"]/div/div[2]/a', describe='选择第一个检索出来的药')
    weights = Elements(xpath='//*[@class="edit_input_box choosed"]/div[2]/input', describe='药品重量')

    drug_methods = Elements(name='chinese_drug_method', describe='用药方法')
    externals = Elements(xpath='//*[@class="charge_address_main externals"]/div[2]/div/a', describe='外用方法')
    brew_flag = Elements(name='brew_flag', describe='煎药方式')
    brewspecs = Elements(xpath='//*[@class="charge_address_main brewSpecs"]/div[2]/div/a', describe='代煎液规格')
    packing_types = Elements(xpath='//*[@class="packing_type"]/div[1]/div[2]/div[1]/a', describe='膏方、丸剂包装类型')
    totle_nums = Elements(xpath='//*[@class="charge_address_main"]/div[2]/div/input', describe='饮片、颗粒共X剂')
    totle_min_tip = Element(xpath='/html/body/div[2]/div[2]', describe='起做量提示')

    signle_nums = Elements(xpath='//*[@class="charge_address_main"]/div[2]/div[3]/select', describe='饮片、颗粒分X次')
    sign_num_opts = Elements(xpath='//*[@class="charge_address_main"]/div[2]/div[3]/select/option',
                             describe='饮片、颗粒分X次下拉选项')
    day_time_opts = Elements(xpath='//*[@name="day_num"]/option', describe='膏方、丸剂每日X次选项')
    can_make_weight = Element(xpath='//*[@class="ouputExplain"]/div/div/div[3]/span', describe='预计出膏X-X克')
    can_use_day = Element(xpath='//*[@class="search_input_box"]/div/div[3]/span', describe='约服X-X天')

    abstains = Elements(xpath='//*[@class="charge_address_main abstain"]/div[2]/div/a', describe='用药禁忌')
    drug_advices = Elements(xpath='//*[@class="charge_address_main"]/div[2]/textarea', describe='医生嘱咐')
    drug_remarks = Elements(xpath='//*[@class="charge_address_main"]/div[2]/textarea', describe='医生嘱咐')

    one_drug_fee = Elements(class_name='one-drug-fee', describe='每剂药价')
    manage_fee = Elements(class_name='manage-fee', describe='管理费')
    service_fee_sel = Element(xpath='//*[@id="drugPage"]/div[3]/div[1]/div[2]/div/select', describe='医事服务费下拉框')
    totle_fee = Element(xpath='//*[@id="drugPage"]/div[3]/div[2]/div/div/span', describe='总价')

    submit_all = Element(id_='submitAll', describe='提交')
    confirm_submit = Element(link_text='确认提交并打印', describe='确认提交并打印')
    got_it = Element(link_text='知道了', describe='知道了')

    # 退出
    user_name = Element(class_name='admin_user_name', describe='当前登录用户')
    logout = Element(class_name='nav_exit', describe='退出系统')
