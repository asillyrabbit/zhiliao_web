from zhiliao.page.backend_page import BackendPage
from zhiliao.auxiliary_tool import AuxiliaryTool
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
import pytest
import time

@pytest.mark.skip()
class TestBackend:

    def test_login(self, browser, base_url, back_account):
        """
        登录：
        1.输入用户名、密码。
        2.验证码截图、识别。
        3.点击登录，验证输入信息。
        4.登录成功跳转页面，失败则继续尝试登录，直到成功。
        """
        try_count = 0
        filename = 'captcha.png'

        global page
        page = BackendPage(browser)
        page.get(base_url[0])

        page.user_name.send_keys(back_account['username'])
        page.pass_word.send_keys(back_account['password'])

        while browser.title != "后台管理":
            # 识别验证码
            if try_count > 0:
                page.captcha.clear()
                page.captcha_image.click()

            browser.save_screenshot(filename)
            captcha_image = browser.find_element_by_id("loginform-captcha-image")
            captcha = AuxiliaryTool().ident_captcha(captcha_image, filename, 100, 30)

            page.captcha.send_keys(captcha)
            page.login_button.click()
            time.sleep(2)
            try_count = try_count + 1

        assert browser.title == "后台管理"

    def test_search_scheduling(self, browser, doc_info):
        """
        医生排班查询：
        1.点击左侧导航“知了诊室”。
        2.点击“出诊医生”。
        3.获取动态表单名，切换表单“ifram”。
        4.根据医生姓名查询。
        5.验证查询结果。
        """
        global yy_count
        page.zl_zhenshi.click()
        page.chuzhe_doc.click()

        # 切换表单
        zs_iframes = page.zs_iframes
        iframe_name = zs_iframes[1].get_attribute("name")

        browser.switch_to.frame(iframe_name)
        # 查询待排班医生
        page.yy_doc_moblie.send_keys(doc_info['mobile'])
        page.zs_sh_button.click()
        time.sleep(1.5)
        yy_count = len(page.yy_count)

        assert yy_count >= 1


    def test_add_scheduling(self, browser, clinic_info, doc_info):
        """
        添加排班：
        (若已有排班，直接返回成功。)
        1.点击添加排班
        2.选择诊所、诊室
        3.设置开放日期、周
        4.设置每个开放时段5个号源
        5.设置预约医生。
        6.断言：返回到排班列表，找到“正常”即认为成功。
        """
        if yy_count > 1 and browser.find_element_by_xpath('//table/tbody/tr[1]/td[8]').text == '正常':
            assert 1 == 1
        else:
            page.add_scheduling.click()
            # 选择诊所、诊室
            clinic_sel = browser.find_element_by_id('consultingroomscheduling-clinic_id')
            Select(clinic_sel).select_by_visible_text(clinic_info['clinic'])
            room_sel = browser.find_element_by_id("consultingroomscheduling-room_id")
            Select(room_sel).select_by_visible_text(clinic_info['room'])

            # 选择开放时间
            page.scheduling_day.click()
            time.sleep(1)
            now_year = time.strftime("%Y", time.localtime())
            now_month = int(time.strftime("%m", time.localtime()))
            now_day = int(time.strftime("%d", time.localtime()))
            lay_ymd = f'[lay-ymd="{now_year}-{now_month}-{now_day}"]'
            sel_now_day = browser.find_element_by_css_selector(lay_ymd)
            ActionChains(browser).move_to_element(sel_now_day).double_click().perform()
            browser.find_element_by_css_selector('[lay-type="confirm"]').click()

            # 选择星期几
            checkboxs = browser.find_elements_by_xpath(
                '//div/ul/li/input[@name="ConsultingRoomScheduling[week_day][]"]')
            weekday = int(time.strftime("%w", time.localtime()))
            checkboxs[weekday - 1].click()

            # 设置每个开放时段5个号源
            for i in range(1, 4):
                t_interval_id = f'consultingroomscheduling-max_count_{i}'
                num_sel = browser.find_element_by_id(t_interval_id)
                Select(num_sel).select_by_visible_text('5')

            page.yy_doc.send_keys(doc_info['mobile'])
            page.temp_name.click()
            page.submits.click()

            assert browser.find_element_by_xpath('//table/tbody/tr[1]/td[8]').text == '正常'

    def test_logout(self, browser,base_url):
        """
        退出系统
        """
        page.get(base_url[0])
        page.logout.click()

        assert browser.title == "登录"


if __name__ == '__main__':
    pytest.main(["-v", "-s"])
