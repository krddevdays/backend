import os
import base64
import json

import dotenv
from django.core.wsgi import get_wsgi_application

dotenv.load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krddevdays.settings')

_application = get_wsgi_application()


def application(environ, start_response):
    api_gateway_context_raw = base64.b64decode(environ.get('HTTP_X_YC_APIGATEWAY_OPERATION_CONTEXT', 'e30=')).decode('utf8')
    api_gateway_context_json = json.loads(api_gateway_context_raw)
    script_name = environ.get('HTTP_X_SCRIPT_NAME', api_gateway_context_json.get('X-Script-Name', ''))
    if script_name:
        environ['SCRIPT_NAME'] = script_name
        path_info = environ['PATH_INFO']
        if path_info.startswith(script_name):
            environ['PATH_INFO'] = path_info[len(script_name):]

    scheme = environ.get('HTTP_X_SCHEME', '')
    if scheme:
        environ['wsgi.url_scheme'] = scheme

    return _application(environ, start_response)
