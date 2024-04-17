import os
import pathlib

from inputs import AwsParameter, parse_input_params
from common.aws_clients import get_client


def run(aws_parameters: dict[str, AwsParameter], input_lambda_name):
    lambda_client = get_client(service_name='lambda',
                               region_name=os.getenv('AWS_REGION'),
                               aws_access_key=os.getenv('AWS_ACCESS_KEY'),
                               aws_secret_key=os.getenv('AWS_SECRET_KEY'),
                               )
    print(aws_parameters, input_lambda_name)


if __name__ == '__main__':
    input_params = os.getenv('INPUT_PARAMS')
    lambda_name = os.getenv('INPUT_LAMBDA_NAME')
    params_inline = parse_input_params(input_params) if input_params is not None else {}
    params_from_file = {}
    params_file_path = os.getenv('INPUT_PARAMS_FILE_PATH')
    if params_file_path is not None and params_file_path != "":
        path = pathlib.PurePath(os.getenv('GITHUB_WORKSPACE'), params_file_path)
        with open(path, 'r') as f:
            params_from_file = parse_input_params(f.read())
    params = {**params_from_file, **params_inline}
    run(params, lambda_name)
