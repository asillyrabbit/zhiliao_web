import tesserocr
import smtplib
import os
import time
import send2trash
import bs4
from PIL import Image
from zhiliao.conftest import REPORT_DIR
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


# 辅助工具
class AuxiliaryTool:

    def temp_page(self, page_object, browser):
        """
        参数：页面对象、驱动。
        1.target_url(被测页面)、cookies，需根据实际情况修改。
        """
        PageObejct = page_object
        target_url = "https://manage.xlyhw.cn/"
        cookies = [
            {
                'name': '_csrf_backend',
                'value': '2791350f00b0190fcdf1a4df97a10d346a4a9d6131a6d673a32920358951a0e1a%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_csrf_backend%22%3Bi%3A1%3Bs%3A32%3A%22S7VIGut0x5TL1Hv8KfVjhO-18mAFyjDY%22%3B%7D'
            },
            {
                'name': 'PHPSESSID',
                'value': 'os8cu1pka4jsc2e1892sl4v4l3'
            }
        ]

        page = PageObejct(browser)
        # 添加cookie前，需先访问一次目标页面，不然会报domain错误。
        page.get(target_url)
        page.add_cookie(cookie_dict=cookies[0])
        page.add_cookie(cookie_dict=cookies[1])
        page.get(target_url)

        return page

    def ident_captcha(self, element, filename, w, h):
        """
        参数：目标元素、截图文件名、元素宽、元素高
        1.找到验证码元素位置。
        2.截图保存。
        3.识别图片上的验证码。
        """
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + w
        bottom = element.location['y'] + h

        image = Image.open(filename)
        image = image.crop((left, top, right, bottom))
        image.save(filename)

        image = Image.open(filename)
        image = image.convert('L')
        threshold = 205  # 指定阀值
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')

        captcha = tesserocr.image_to_text(image).strip()

        return captcha

    def delete_report(self):
        """
        删除测试报告文件夹
        """
        os.chdir(REPORT_DIR)
        now_year = time.strftime("%Y")

        for file in os.listdir():
            if file.startswith(now_year):
                send2trash.send2trash(file)

    def failed_case(self):
        """
        返回日报路径、失败用例名、失败截图名
        """
        os.chdir(REPORT_DIR)
        now_year = time.strftime("%Y")

        file_dir = ''
        for file in os.listdir():
            if file.startswith(now_year):
                file_dir = file
                os.chdir(file_dir)

        report_file = open('report.html', encoding='utf-8')
        report_soup = bs4.BeautifulSoup(report_file, "html.parser")
        failed_rows = report_soup.select('#results-table .failed')

        failed_case = []
        failed_img = []
        for failed_row in failed_rows:
            col_name = failed_row.select('.col-name')
            img = failed_row.select('img')
            image_name = str(img[0].get('src'))

            case_name = str(col_name[0].text)

            if '异常' in case_name:
                continue
            else:
                failed_case.append(case_name)
                failed_img.append(image_name)

        return file_dir, failed_case, failed_img

    def send_email(self, from_email, to_emails):
        """
        发送邮件，正文内容：失败用例名+失败用例截图
        """

        # 失败用例相关信息
        failed_case = self.failed_case()

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header("知了有方测试团队", 'utf-8')
        subject = '知了Web UI自动化测试报告'
        message['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        content = f'<h3>失败用例：</h3>'
        for name in failed_case[1]:
            name = f'<p>{name}</p>'
            content = content + name

        body_msg = f'<div>{content} <img src="cid:image"/></div>'

        os.chdir(REPORT_DIR)

        for img in failed_case[2]:
            img_data = open(failed_case[0] + '/' + img, 'rb').read()
            html_part = MIMEMultipart(_subtype='related')
            body = MIMEText(body_msg, _subtype='html')
            html_part.attach(body)

            msg_img = MIMEImage(img_data, 'png')
            msg_img.add_header('Content-Id', '<image>')
            msg_img.add_header('Content-Disposition', 'inline', filename=('utf-8', '', img))
            html_part.attach(msg_img)
            message.attach(html_part)

        # 连接到SMTP服务器
        smtpObj = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)

        # 登录发送邮箱
        smtpObj.login(from_email[0], from_email[1])

        # 发送
        smtpObj.sendmail(from_email[0], to_emails, message.as_string())

        # 从SMTP服务器断开
        smtpObj.quit()

    def bak(self):
        """
        用例名中文乱码时，解码方法
        """
        file_name = 'test_staff.py_TestStaff_test_register[新号+新患者+身份证+男+异常].png].png'
        print(file_name.encode('utf-8').decode('iso-8859-1'))
