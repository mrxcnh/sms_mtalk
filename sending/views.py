from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import FormView

from sending import utils
from sending.forms import UploadFileForm


class UploadFile(FormView):
    template_name = 'upload_csv.html'
    form_class = UploadFileForm

    def form_valid(self, form):

        data_file = form.cleaned_data['data_file']
        data_rows = utils.get_data_form_excel_file(data_file)

        for data_row in data_rows:
            no = data_row['No']
            campaign = data_row['Campaign']
            campaign_code = data_row['Campaign code']
            link_campaign = data_row['Link campaign']
            content = data_row['Content']
            phone = data_row['Phone']
            sms_status = data_row['SMS status']
            tracking_report = data_row['Tracking report']
            pic = data_row['PIC']
            sale_status = data_row['Sale status']

            if utils.isValid(phone):
                phone_number = utils.process_number(phone)
            else:
                return HttpResponse(f'Invalid-phone number-can not send to:+84{phone} in No:{no}')

            url = utils.encode_url_phone(settings.HOST, link_campaign, phone)
            body = content.replace(link_campaign, url)
            sms_data = {
                'campaign': campaign,
                'campaign_code': campaign_code,
                'link_campaign': link_campaign,
                'content': body,
                'phone': phone,
                'sms_status': sms_status,
                'tracking_report': tracking_report,
                'pic': pic,
                'sale_status': sale_status
            }
            utils.create_sms(**sms_data)
            try:
                utils.send(phone_number, body)
            except Exception as e:
                return HttpResponse(f'Message Error: {e}')
        return HttpResponse(f'Messages sent successfully')

    def form_invalid(self, form):
        return HttpResponse(f'Invalid file')


class TrackingAccessURL(View):
    def get(self, request):
        url = request.GET.get('url')
        phone = request.GET.get('phone')
        sms = utils.get_sms_with_url_phone(link_campaign=url, phone=phone)

        if sms is None:
            return HttpResponseRedirect(url)

        sms.visit_count += 1
        sms.save()
        return HttpResponseRedirect(url)
