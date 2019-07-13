from django.http import HttpResponse
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
            link_campaign = data_row['Link campaign']
            content = data_row['Content']
            phone = data_row['Phone']

            if not utils.isValid(phone):
                return HttpResponse(f'Invalid-phone number-can not send to:+84{phone} in No:{no}')

            phone_number = utils.process_number(phone)
            url = utils.encode_url_phone(link_campaign, phone)
            body = content.replace(link_campaign, url)
            a = body

    def form_invalid(self, form):
        return HTTPResponse(f'Invalid file')
