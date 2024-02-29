import jinja2
import subprocess
import os
import boto3
from datetime import datetime
from common_component.src.core.utils.Logger import logger
from common_component.src.core.helpers.s3_helper import download_file_from_s3, upload_file_to_s3
from common_component.src.core.helpers.ssm_helper import get_ssm_parameter

# Create client for parameter store and s3
ssm_client = boto3.client('ssm', region_name='ca-central-1')
s3_resource = boto3.resource('s3', region_name='ca-central-1')


def create_pdf(html_template_file_name, pdf_title, output_file_name, json_data):
    bucket = get_ssm_parameter('/pic/application/bucket_name')
    try:
        file_key = get_ssm_parameter('/pic/pdf/survey/file_key')
        local_file_path = file_key.replace('email/attachment/pdf/', '/tmp/')
        pdf_template_name = download_file_from_s3(bucket, file_key, local_file_path)

        logo_file_key = get_ssm_parameter('/pic/pdf/survey/logo_file_key')
        logo_local_file_path = logo_file_key.replace('email/attachment/pdf/', '/tmp/')
        download_file_from_s3(bucket, logo_file_key, logo_local_file_path)

        wkhtmltopdf_options = {'orientation': 'portrait', 'title': pdf_title}
        template_loader = jinja2.FileSystemLoader(searchpath="/tmp")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = pdf_template_name.replace("/tmp/", "")

        template = template_env.get_template(template_file)

        html_template = template.render(dynamicData=json_data)

        with open(html_template_file_name, 'w') as f:
            f.write(html_template)
        command = 'wkhtmltopdf --javascript-delay 1000 --no-stop-slow-scripts --enable-javascript --debug-javascript --enable-local-file-access --load-error-handling ignore'  # ignore unecessary errors
        for key, value in wkhtmltopdf_options.items():
            if key == 'title':
                value = f'"{value}"'
            command += ' --{0} {1}'.format(key, value)
        command += ' {0} {1}'.format(html_template_file_name, output_file_name)
        try:
            subprocess.run(command, shell=True)

            current_timestamp = datetime.now().strftime('%Y%m%d')
            current_file_name = os.path.basename(output_file_name)
            s3_file_name = 'email/attachment/pdf/' + current_timestamp + '/' + current_file_name
            return upload_file_to_s3(output_file_name, s3_file_name, bucket)
        except Exception as e:
            logger.info('Exception occurred while creating pdf : ' + str(e))
    except Exception as e:
        logger.info('Exception occurred while creating pdf : ' + str(e))
