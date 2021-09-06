from PIL import Image
import tesserocr


# 辅助工具
class AuxiliaryTool:

    def temp_page(self, page_object, browser):
        """
        参数：页面对象、驱动。
        1.target_url(被测页面)、cookies，需根据实际情况修改。
        """
        PageObejct = page_object
        target_url = "http://zhenshi.testing.xlyhw.com/drugdoc/drug?patientid=2880661&order_no=2109033783490817"
        cookies = [
            {
                'name': '_csrf',
                'value': '10eb4010417b12933fa0fa2a2933833529a3623dcebcc9eeaf8681d5fd5c4801a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22w%DCfc%EFc%3A%1F%82VL%E0k%3A%5C%95%80%CEF%97%D5%C72z%28%21j%F4%94%F2N%C9%22%3B%7D'
            },
            {
                'name': 'PHPSESSID',
                'value': '61317eb3b42d5'
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
