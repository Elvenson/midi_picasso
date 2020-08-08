# Copyright 2020 Bui Quoc Bao.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Midi Picasso script."""

import logging
import argparse
import configs

LOGGER = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'


def parse_arg():
    """
    Parses parameters for execution.
    :return: ParsedArgument object contains script parameters.
    """
    parser = argparse.ArgumentParser()

    # Input argument.
    parser.add_argument(
        '--verbosity',
        choices=[
            'DEBUG',
            'ERROR',
            'FATAL',
            'INFO',
            'WARN',
        ],
        default='INFO',
        help='Set logging verbosity',
    )
    parser.add_argument(
        '--config',
        help='Config name for creating art style',
        default='freestyle',
        type=str,
    )
    parser.add_argument(
        '--input',
        help='Midi input path file',
        type=str,
        required=True,
    )
    parser.add_argument(
        '--output',
        help='Output image file name',
        type=str,
        required=True,
    )
    parsed_args = parser.parse_args()
    return parsed_args


def run(params):
    """
    Encodes midi into image according to style.
    :param params: a Config object contains all required parameters.
    :return:
    """
    config_update_map = dict()
    config_update_map['input'] = params.input
    config_update_map['output'] = params.output
    conf = configs.CONFIG_MAP[params.config]
    conf = configs.update_config(conf, config_update_map)
    encoder_style = conf.encoder_style
    encoder_style.encode_midi(conf.input, conf.output, conf.style_params)


if __name__ == '__main__':
    args = parse_arg()
    logging.basicConfig(level=getattr(logging, args.verbosity),
                        format=LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    run(args)
