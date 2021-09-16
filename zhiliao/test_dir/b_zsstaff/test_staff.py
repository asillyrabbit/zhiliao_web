from zhiliao.page.staff_page import StaffPage
from zhiliao.auxiliary_tool import AuxiliaryTool
from selenium.webdriver.support.select import Select
import pytest
import random

from zhiliao.test_dir.b_zsstaff.conftest import pat_info


@pytest.mark.skip()
class TestStaff:

    def test_login(self, browser, base_url, staff_account):
        """
        1.选择员工登录。
        2.该处有个bug，第一次登录无法成功，所以连续登录2次。
        3.断言判断挂号登录菜单存在即为成功。
        """
        global page

        page = StaffPage(browser)
        page.get(base_url[1])

        page.login_id.click()
        page.username.send_keys(staff_account['username'])
        page.password.send_keys(staff_account['password'])
        page.login_btn.click()

        assert page.register_menu

    @pytest.mark.parametrize("pat_info",
                             pat_info,
                             ids=[pat_info[i]['title'] for i in range(len(pat_info))])
    def test_register(self, browser, base_url, doc_info, pat_info):
        """
        1.点击登记进入挂号页面。
        2.读取参数文件，判断是老患者还是新患者。
        3.如果是老患者，输入完手机号之间填写挂号信息。
        4.如果是新患者，完成患者信息、挂号信息填写。
        5.提交，在付费页面随机选择一种付费方式（除POS机外）。
        6.点击打印挂号单确认按钮。
        7.断言判断返回挂号列表页，且找到已到店标识即认为成功。
        """
        # 切换到挂号登记页面
        page.get(base_url[1])
        page.register_menu.click()
        frame = page.st_frame.get_attribute("id")
        browser.switch_to.frame(frame)
        page.patient_register.click()

        # 患者信息
        page.patient_mobile.send_keys(pat_info['mobile'])
        # 判断是否有老患者，有则选择返回的第一个老患者
        old_flag = 'NO'
        try:
            browser.find_element_by_id('patientList')
            old_flag = 'YES'
        except:
            pass

        if old_flag == 'YES' and pat_info['p_type'] == 'old':
            page.first_patient.click()
        else:
            page.patient_name.send_keys(pat_info['name'])
            sel_gender = browser.find_element_by_id('gender')
            Select(sel_gender).select_by_visible_text(pat_info['gender'])
            page.birthday.send_keys(pat_info['birthday'])

            # 判断是否为居民身份证
            if len(pat_info['id_card']) < 18:
                sel_card_type = browser.find_element_by_name('card_type')
                random_opt = random.randint(1, 6)
                name_xpah = f'//*[@name="card_type"]/option[{random_opt}]'
                card_type = browser.find_element_by_xpath(name_xpah).text
                Select(sel_card_type).select_by_visible_text(card_type)

            page.id_card.send_keys(pat_info['id_card'])

        # 挂号信息
        sel_doc = browser.find_element_by_id('schedDoctor')
        Select(sel_doc).select_by_visible_text(doc_info['name'])
        sel_sch = browser.find_element_by_id('scheduling')
        sch_opt = browser.find_element_by_xpath('//*[@id="scheduling"]/option[2]').text
        Select(sel_sch).select_by_visible_text(sch_opt)
        page.jz_time_div.click()
        jz_times = page.jz_times

        # 找到没约满的时段进行预约
        for i in range(len(jz_times)):
            if jz_times[i].text.endswith('（已约满）'):
                continue
            else:
                jz_times[i].click()
                break

        page.re_submit.click()
        # 支付方式，随机选择现金、企业支付、对公支付
        pay_types = page.pay_types
        lis_index = [0, 2, 3]
        sel_index = random.choice(lis_index)
        pay_types[sel_index].click()
        if sel_index != 0:
            page.pay_input.send_keys('自动化测试')
        page.fee_confirm.click()
        page.fee_confirm_submit.click()

        # 找到”已到店“即判定为已返回挂号列表页，即判定为成功
        assert page.result.text == '已到店'

    def test_logout(self, browser, base_url):
        page.get(base_url[1])
        page.login_name.click()
        page.logout.click()

        assert browser.title != '知了诊室'


if __name__ == '__main__':
    pytest.main()
