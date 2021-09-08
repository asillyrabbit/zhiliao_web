from zhiliao.page.doctor_page import DoctorPage
from zhiliao.auxiliary_tool import AuxiliaryTool
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import pytest
import time
import random

from zhiliao.test_dir.c_zsdoc.conftest import drug_infos, basic_infos


# @pytest.mark.skip()
class TestDoctor:

    def test_login(self, browser, base_url, doc_info):
        """
        1.选择密码登录方式。
        2.输入医生手机号、密码，点击登录。
        3.点击选择诊所弹窗页确认按钮。
        4.断言“门诊患者”存在即为成功。
        """
        global page
        page = DoctorPage(browser)
        page.get(base_url[1])
        page.login_doctor_pwd.click()
        page.doctor_mobile.send_keys(doc_info['mobile'])
        page.doctor_password.send_keys(doc_info['password'])
        page.clinic_login.click()
        page.select_clinic_determine.click()

        assert page.pat_menu

    def reception(self, page):
        """
        接诊：直接接诊
        再次开方：随机选择一条
        """
        if page.first_row.text == "接诊":
            page.first_row.click()
            page.jz_confirm.click()
        else:
            rows = page.jz_rows
            if len(rows) == 1:
                rows[0].click()
            else:
                rows[random.randint(0, len(rows) - 1)].click()

    def basic_info(self, page, basic_infos):
        """
        基础信息：诊断、辨证、主诉、过敏史、同期服用药物
        """
        page.diagnosis.clear()
        page.diagnosis.send_keys(basic_infos['zhen_duan'])
        page.dialectical.clear()
        page.dialectical.send_keys(basic_infos['bian_zheng'])
        page.complaint.clear()
        page.complaint.send_keys(basic_infos['zhu_su'])
        page.allergy.clear()
        page.allergy.send_keys(basic_infos['guo_ms'])
        page.medicine.clear()
        page.medicine.send_keys(basic_infos['tong_qfy'])

    def drug_select(self, page, drug_infos):
        """
        剂型选择
        """
        drug_type = drug_infos['drug_type']
        drug_selects = page.drug_selects
        drug_select = drug_selects[2]
        Select(drug_select).select_by_visible_text(drug_type)
        if drug_type == "配方颗粒":
            page.change_confirm.click()
        time.sleep(1.5)

    def sup_select(self, page, drug_infos):
        """
        药房选择
        """
        sup_name = drug_infos['sup_name']
        sup_selects = page.sup_selects
        sup_select = sup_selects[1]
        Select(sup_select).select_by_visible_text(sup_name)

    def add_drugs(self, page, browser, drug_infos):
        """
        添加药品
        """
        flag_num = 0
        scrollTop = 210
        for name, weight in drug_infos['details'].items():
            input_drug_names = page.input_drug_names
            input_drug_names[-1].send_keys(name)
            time.sleep(1.5)

            sel_drugs = page.sel_drugs
            for sel_drug in sel_drugs:
                if sel_drug.text == name:
                    sel_drug.click()
                    break
            time.sleep(1.5)
            weights = page.weights
            weights[-1].send_keys(weight)
            flag_num += 1
            # 每添加4味药，左侧滚动条向下滚动210px
            if flag_num % 4 == 0:
                pos_js = f'document.getElementsByClassName("main-js")[2].scrollTop={scrollTop}'
                browser.execute_script(pos_js)
                scrollTop += 210
                time.sleep(1.5)

    def attention_remark(self, page):
        """
        用药禁忌、医生嘱咐、药房备注
        """
        # 用药禁忌：随机选择3个
        abstains = page.abstains
        for i in range(0, 3):
            abstains[random.randint(len(abstains) / 2, len(abstains) - 1)].click()
        advices = page.drug_advices
        advices[3].send_keys("早餐前2小时，用淡盐水送服。")
        remarks = page.drug_remarks
        remarks[4].send_keys("测试订单，不用放处方。")

    def yinpian_keli_special(self, page, browser, drug_infos):
        """
        中药饮片：内服（med_type=0）、外用（med_type=1）
        参数代煎规格、分X次服用为检查点。
        """
        med_type = drug_infos['med_type']

        if med_type == 1:
            page.drug_methods[1].click()
            # 外用方法：随机选3个，存在选中又取消的情况，最终至少会选中1个
            externals = page.externals
            for i in range(0, 3):
                externals[random.randint(0, len(externals) - 1)].click()

        if drug_infos['drug_type'] == "中药饮片":
            # 煎药方式
            bre_flag = drug_infos['brew_flag']
            page.brew_flag[bre_flag].click()
            # 代煎液规格：先判断返回列表与药厂实际规格是否一致，然后随机选择一个规格
            brewspecs = page.brewspecs
            brew_list = []
            for brew in brewspecs:
                brew_list.append(brew.text)
            if drug_infos['brew_list'] == brew_list:
                brewspecs[random.randint(0, len(brewspecs) - 1)].click()
            else:
                return "fail：代煎规格与该药房实际规格不符！"

        # 左侧滚动条滚到底
        pos_js = f'document.getElementsByClassName("main-js")[2].scrollTop=1000'
        browser.execute_script(pos_js)
        # 共多少剂：有默认值，不能用clear，可以先全选，然后再输入
        totle_num = page.totle_nums[1]
        totle_num.send_keys(Keys.CONTROL, 'a')
        totle_num.send_keys(drug_infos['tot_num'])

        # 分X次服用：先检查下拉框中选项是否与对应药房的实际规格一致
        num_list = []
        sign_num_opts = page.sign_num_opts
        sign_num_opts = sign_num_opts[4:]
        for num_opt in sign_num_opts:
            num_list.append(num_opt.text)
        sign_num = drug_infos['sign_num']
        if sign_num == num_list:
            signle_nums = page.signle_nums
            Select(signle_nums[1]).select_by_visible_text(random.choice(sign_num))
        else:
            return "fail：分X次服用选项与该药房实际规格不符！"

        return "pass"

    def gaofang_miwan_special(self, page, browser, drug_infos):
        """
        参数辅料重量、包装类型为检查点。
        """
        # 膏方辅料
        drug_type = drug_infos['drug_type']
        if drug_type == "滋补膏方":
            sel_list = []
            # 辅料种类，按6种设计
            for i in range(1, 7):
                name = f'addnum{i}'
                sel_element = browser.find_element_by_name(name)
                sel_list.append(sel_element)
            for i in range(0, 2):
                sel_opt = sel_list[random.randint(0, len(sel_list) - 1)]
                Select(sel_opt).select_by_visible_text(random.choice(drug_infos['weights']))
            # 包装
            pack_type_list = []
            packing_types = page.packing_types
            for packing_type in packing_types:
                pack_type_list.append(packing_type.text)

            if pack_type_list == drug_infos['pack_types']:
                packing_types[random.randint(0, len(pack_type_list) - 1)].click()
            else:
                return "fail：包装类型与该药房实际规格不符！"
        # 剂量用法
        time.sleep(1.5)
        take_day = drug_infos['take_day']
        day_time_opts = page.day_time_opts
        day_time_opt = day_time_opts[random.randint(0, len(day_time_opts) - 1)].text
        day_time_sel = browser.find_element_by_xpath('//*[@name="day_num"]')
        Select(day_time_sel).select_by_visible_text(day_time_opt)
        time_takes = browser.find_elements_by_xpath('//*[@name="signle_num"]')
        time_take = time_takes[1]
        time_take.send_keys(Keys.CONTROL, 'a')
        time_take.send_keys(take_day)

        # 左侧滚动条滚到底
        pos_js = f'document.getElementsByClassName("main-js")[2].scrollTop=1000'
        browser.execute_script(pos_js)

        # 验证约膏方服X~X天
        if drug_type == "滋补膏方":
            can_make_weight = page.can_make_weight
            can_make = can_make_weight.text
            can_make_list = can_make.split('~')
            c_m_1 = can_make_list[0].strip('g')
            c_m_2 = can_make_list[1].strip('g')
            can_use_day = page.can_use_day
            can_use = can_use_day.text
            can_use_list = can_use.split('~')
            c_u_1 = can_use_list[0]
            c_u_2 = can_use_list[1]
            result_1 = (int(c_m_1) / int(day_time_opt)) / int(take_day)
            result_2 = (int(c_m_2) / int(day_time_opt)) / int(take_day)

            if int(result_1) != int(c_u_1) and int(result_2) != int(c_u_2):
                return "fail:约服天数不正确！"

        return "pass"

    def drug_special(self, page, browser, drug_infos):
        drug_type = drug_infos['drug_type']
        if drug_type == "中药饮片" or drug_type == "配方颗粒":
            result = self.yinpian_keli_special(page, browser, drug_infos)
        else:
            result = self.gaofang_miwan_special(page, browser, drug_infos)
        return result

    def check_total_price(self, page, browser, drug_infos):
        from decimal import Decimal
        one_fee_list = page.one_drug_fee
        one_drug_fee = one_fee_list[1].text
        m_fee_list = page.manage_fee
        manage_fee = m_fee_list[1].text
        s_fee_sel = browser.find_element_by_xpath('//*[@id="drugPage"]/div[3]/div[1]/div[2]/div/select')

        service_fee = Select(s_fee_sel).first_selected_option.text
        service_fee = service_fee.split("元")[0]

        # 药品总价
        drug_fee = Decimal(one_drug_fee) * Decimal(drug_infos['tot_num'])
        fee_list = browser.find_elements_by_xpath('//*[@id="drugPage"]/div[3]/div/div/div/span')

        if drug_infos['drug_type'] == "滋补膏方" or drug_infos['drug_type'] == "蜜丸":
            make_fee = fee_list[3].text
        else:
            make_fee = '0'

        totle_fee = Decimal(fee_list[0].text)
        all_fee = Decimal(drug_fee) + Decimal(make_fee) + Decimal(manage_fee) + Decimal(service_fee)

        if all_fee == totle_fee:
            return "pass"
        else:
            return "fail:总价不正确！"

    @pytest.mark.parametrize("basic_infos", basic_infos)
    @pytest.mark.parametrize("drug_infos", drug_infos,
                             ids=[drug_infos[i]['title'] for i in range(len(drug_infos))])
    def test_drug(self, browser, base_url, drug_infos, basic_infos):
        """
        1.接诊、再次开方。
        2.开方。
        3.结果集验证（剂型特性、价格、提交后跳转）。
        """
        # 结果集
        results = []

        # 切换iframe
        page.get(base_url[1])
        frame = page.frame.get_attribute("id")
        browser.switch_to.frame(frame)

        # 接诊
        self.reception(page)

        # 诊断等基础信息，选择剂型、药房，添加药材
        self.basic_info(page, basic_infos)
        self.drug_select(page, drug_infos)
        self.sup_select(page, drug_infos)
        self.add_drugs(page, browser, drug_infos)

        # 剂型特性
        result = self.drug_special(page, browser, drug_infos)
        results.append(result)

        # 禁忌、备注等
        self.attention_remark(page)
        result = self.check_total_price(page, browser, drug_infos)
        results.append(result)

        # 提交
        page.submit_all.click()
        page.confirm_submit.click()
        page.got_it.click()

        # 提交后跳转验证
        if page.created_prescription:
            result = "pass"
        else:
            result = "fail：没有正确跳转回接诊列表页。"
        results.append(result)

        # 验证结果集
        assert "fail" not in str(results)

    # @pytest.mark.skip()
    def test_logout(self, browser, base_url):
        """
        退出系统
        """
        page.get(base_url[1])
        page.user_name.click()
        page.logout.click()

        assert browser.title == "知了诊室-登录"


if __name__ == '__main__':
    pytest.main(['-v', '-s'])
