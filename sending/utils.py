from twilio.rest import Client
from xlrd import open_workbook


def send(phone, body):
    account_sid = 'account SID need to change for sending message'
    auth_token = 'authenticate token need to change for sending message'
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

    if count_char > 13:
        return False
    if count_char < 11:
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


def encode_url_phone(url, phone) -> str:
    return f'{url}{phone}'
