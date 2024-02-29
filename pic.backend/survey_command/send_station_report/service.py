import boto3
import json
from common_component.src.component.common_services.services import outlet_service 
from  common_component.src.component.common_services.services.survey_schedule_service import get_survey_schedule_mail_header, get_survey_schedule_detail_by_site_id
from datetime import datetime
from common_component.src.core.utils.Logger import logger
from schemas.survey_scheduel_schema import SendStationReportTemplate, StationReportList
from common_component.src.core.helpers.ssm_helper import get_ssm_parameter
from common_component.src.core.helpers.pdf_helper import create_pdf
from common_component.src.core.helpers.sqs_helper import send_msg_to_sqs
from common_component.src.core.repositories.data_repository import CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.resources.constants import ServiceName
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service(ServiceName.SURVEY_SCHEDULE_SERVICE_NAME.value)


# Create client for parameter store and s3
ssm_client = boto3.client('ssm', region_name='ca-central-1')
s3_resource = boto3.resource('s3', region_name='ca-central-1')


def send_pdf_using_email(station_report_list: StationReportList):
    try:
        log.append_keys(service_function="send_pdf_using_email")
        log.debug("Entered into send_pdf_using_email service")
        site_id_success = []
        site_id_failure = []
        val = json.loads(station_report_list.json())

        if len(val['station_report_list']) == 1:
            response = generate_pdf_template(val['station_report_list'][0], True, val['language'], val['user_id'],
                                             val['request_date'], val['include_rows'])
            if response['statusCode'] == 200:
                site_id_success.append(val['station_report_list'][0]['outlet_id'])
            else:
                site_id_failure.append(val['station_report_list'][0]['outlet_id'])
        else:
            for site_data in val['station_report_list']:
                response = generate_pdf_template(site_data, False, val['language'], val['user_id'], val['request_date'],
                                                 val['include_rows'])

                if response['statusCode'] == 200:
                    site_id_success.append(site_data['outlet_id'])
                else:
                    site_id_failure.append(site_data['outlet_id'])

        response = {
            "status_code": 200,
            "message": "Sent email to all site ID's successfully",
            "data": {"survey_schedule_send_email": {
                "success_site_id_list": site_id_success,
                "error_site_id_list": site_id_failure
            }
            }
        }
    except Exception as exc:
        raise exc
    else:
        log.debug("send_pdf_using_email service executed successfully")
        return response


def generate_pdf_template(send_station_report_template: SendStationReportTemplate, single_row: bool, language: str,
                          user_id: str, request_date: datetime, include_rows: bool):
    try:
        log.append_keys(service_function="generate_pdf_template")
        log.debug("Entered into generate_pdf_template service")
        competitor_status = 1 if send_station_report_template['status'] else 0
        include_rows = 1 if include_rows else 0

        get_survey_schedule_detail_data = get_survey_schedule_detail_by_site_id(
            send_station_report_template['outlet_id'],
            request_date,
            competitor_status,
            include_rows,
            language)

        get_survey_schedule_detail_data = get_survey_schedule_detail_data['data']['survey_schedule_list']

        get_outlet_detail_by_site_id_data = outlet_service.get_outlet_detail_by_site_id(
            send_station_report_template['outlet_id'], language, user_id)

        get_outlet_detail_by_site_id_data = get_outlet_detail_by_site_id_data['data']['outlet_detail_by_site_no']

        get_survey_schedule_mail_header_data = get_survey_schedule_mail_header(
            send_station_report_template['outlet_id'], language, user_id)

        get_survey_schedule_mail_header_data = get_survey_schedule_mail_header_data['data'][
            'survey_schedule_mail_header']

        note1 = get_survey_schedule_mail_header_data['note1']
        note2 = get_survey_schedule_mail_header_data['note2']
        file_name_initial = get_survey_schedule_mail_header_data['file_name']

        # table data for gas
        row_data_gas = {}
        table_data_gas_obj = []
        for obj in get_survey_schedule_detail_data:
            if obj['product_id'] == 2:
                row_data_gas['frequency'] = obj['frequency_values']
                row_data_gas['competitors'] = str(obj['kent_id'])
                row_data_gas['address'] = obj['address']
                row_data_gas['brand_marketer'] = obj['brand_marketer']
                row_data_gas['time1'] = ' - '
                row_data_gas['time2'] = ' - '
                row_data_gas['time3'] = ' - '
                row_data_gas['time4'] = ' - '
                row_data_gas['time5'] = ' - '
                for time_slot in obj['json_time_list']:
                    if row_data_gas['time' + str(time_slot['display_number'])] == ' - ':
                        row_data_gas['time' + str(time_slot['display_number'])] = str(time_slot['from']) + ' - ' + \
                                                                                  str(time_slot['to'])
                table_data_gas_obj.append(row_data_gas)
                row_data_gas = {}

        table_data_gas = ''
        for obj in table_data_gas_obj:
            table_data_gas += "<tr><td></td><td>" + obj['frequency'] + "</td><td>" + obj['competitors'] + "</td><td>" +\
                              obj['address'] + "</td><td>" + obj['brand_marketer'] + "</td><td>" + obj[
                                  'time1'] + "</td><td>" + obj['time2'] + "</td><td>" + obj['time3'] + "</td><td>" + \
                              obj['time4'] + "</td><td>" + obj['time5'] + "</td></tr>"

        # table data for diesel
        row_data_diesel = {}
        table_data_diesel_obj = []
        for obj in get_survey_schedule_detail_data:
            if obj['product_id'] == 4:
                row_data_diesel['frequency'] = obj['frequency_values']
                row_data_diesel['competitors'] = str(obj['kent_id'])
                row_data_diesel['address'] = obj['address']
                row_data_diesel['brand_marketer'] = obj['brand_marketer']
                row_data_diesel['time1'] = ' - '
                row_data_diesel['time2'] = ' - '
                row_data_diesel['time3'] = ' - '
                row_data_diesel['time4'] = ' - '
                row_data_diesel['time5'] = ' - '
                for time_slot in obj['json_time_list']:
                    if row_data_diesel['time' + str(time_slot['display_number'])] == ' - ':
                        row_data_diesel['time' + str(time_slot['display_number'])] = str(
                            time_slot['from']) + ' - ' + str(
                            time_slot['to'])
                table_data_diesel_obj.append(row_data_diesel)
                row_data_diesel = {}

        table_data_diesel = ''
        for obj in table_data_diesel_obj:
            table_data_diesel += "<tr><td></td><td>" + obj['frequency'] + "</td><td>" + obj[
                'competitors'] + "</td><td>" + \
                                 obj['address'] + "</td><td>" + obj['brand_marketer'] + "</td><td>" + \
                                 obj['time1'] + "</td><td>" + obj['time2'] + "</td><td>" + obj['time3'] + "</td><td>" +\
                                 obj['time4'] + "</td><td>" + obj['time5'] + "</td></tr>"

        current_date = datetime.now().strftime('%Y-%m-%d %I:%M')
        territory_manager = get_outlet_detail_by_site_id_data['territory_manager']
        regional_operating_manager = get_outlet_detail_by_site_id_data['regional_office_manager']
        site_name = get_outlet_detail_by_site_id_data['display_name']

        json_data = {
            "table_data_gas": table_data_gas,
            "table_data_diesel": table_data_diesel,
            "territory_manager": territory_manager,
            "regional_operating_manager": regional_operating_manager,
            "site_name": site_name,
            "date": current_date,
            "note1": note1,
            "note2": note2
        }

        title_ext = datetime.now().strftime('%Y%m%d%I%M')
        pdf_title = file_name_initial + "-" + str(send_station_report_template['outlet_id']) + title_ext
        html_template_file_name = '/tmp/pic_temp' + title_ext + '.html'
        output_file_name = '/tmp/' + pdf_title + '.pdf'
        s3_pdf_file_name = create_pdf(html_template_file_name, pdf_title, output_file_name, json_data)

        # create email object
        email_data = {
            'service_name': 'survey_schedule_service',
            'to_addresses': get_outlet_detail_by_site_id_data['station_email'],
            'email_subject': get_survey_schedule_mail_header_data['subject'],
            'email_body': get_survey_schedule_mail_header_data['body'],
            'attachment': s3_pdf_file_name
        }

        if single_row:
            email_data = {
                'service_name': 'survey_schedule_service',
                'to_addresses': send_station_report_template['to'],
                'email_subject': get_survey_schedule_mail_header_data['subject'],
                'email_body': send_station_report_template['message'],
                'attachment': s3_pdf_file_name
            }

        queue_name = get_ssm_parameter('/pic/email/parameters/queue_name')
        email_data['to_addresses'] = email_data['to_addresses'].replace(";", ",")
        # add send email function
        email_data = str(email_data)
        send_email_response = send_msg_to_sqs(queue_name, email_data)

    except Exception as e:
        error_message = f"An error occurred in generate_pdf_template function : {str(e)}"
        logger.info(error_message)
        raise e
    else:
        log.debug("generate_pdf_template service executed successfully")
        return jsonable_encoder(send_email_response)
