from django.conf import settings
from twilio.rest import Client
from xlrd import open_workbook

from sending import models

DIGIT_OFFSET = 38


def send(phone, body):
    account_sid = settings.account_sid
    auth_token = settings.auth_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+447480778396',
        body=body,
        to='+84'+phone
    )
    return message


def isValid(s):
    count = 0
    count_char = 0

    for char in s:
        count_char += 1
        if not char.isdigit():
            count += 1

    if count_char > 10:
        return False
    if count_char < 8:
        return False
    if count > 1:
        return False
    else:
        return True


def process_number(phone_number):
    if phone_number[0] is '0':
        phone = phone_number[1:]

    elif phone_number[0] is '+':
        phone = phone_number[3:]

    else:
        phone = phone_number

    return phone


def get_data_form_excel_file(data_file):
    wb = open_workbook(file_contents=data_file.read())
    data_rows = []
    for sheet in wb.sheets():
        if sheet.nrows < 1:
            break
        for row in range(1, sheet.nrows):
            col_value = {}
            for col in range(sheet.ncols):
                value = (sheet.cell(row, col).value)
                try:
                    value = str(int(value))
                except:
                    pass
                col_value.update({sheet.cell(0, col).value: value})
            data_rows.append(col_value)

    wb.release_resources()
    del wb
    return data_rows


def true_ord(char):
    return ord(char) - DIGIT_OFFSET


def encode_url_phone(host: str = '', url: str = '', phone: str = '') -> str:
    return f'{host}?url={url}&phone={phone}'


def decode_url_phone(encoded_url: str = '') -> dict:
    return {
        'url': '/'.join(encoded_url.split('/')[0:-1]),
        'phone': encoded_url.split('/')[-1]
    }


def create_sms(*, campaign: str = '', campaign_code: str = '',
               link_campaign: str = '', content: str = '',
               phone: str = '', sms_status: str = '',
               tracking_report: str = '', pic: str = '',
               sale_status: str = '', visit_count: int = 0):
    sms = models.SMS(
        campaign=campaign,
        campaign_code=campaign_code,
        link_campaign=link_campaign,
        content=content,
        phone=phone,
        sms_status=sms_status,
        tracking_report=tracking_report,
        pic=pic,
        sale_status=sale_status,
        visit_count=visit_count
    )
    sms.save()
    return sms


def get_sms_with_url_phone(link_campaign: str = '', phone: str = ''):
    return models.SMS.objects.filter(link_campaign=link_campaign, phone=phone).first()

