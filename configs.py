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

"""Midi Picasso configs"""
import collections
from styles.freestyle import FreeStyle


class GeneralParams(collections.namedtuple(
        'GeneralParams', ['use_drum', 'sustain', 'max_length',
                          'width', 'height', 'scale', 'shape'])):
    """General params for all styles."""

    def values(self):
        """Returns params as dictionary."""
        return self._asdict()


class Config(collections.namedtuple(
        'Config', ['style_params', 'encoder_style', 'input', 'output'])):
    """Config class for storing configs."""

    def values(self):
        """Returns config as dictionary."""
        return self._asdict()


def update_config(config, update_dict):
    """Updates old config with new values."""
    config_dict = config.values()
    config_dict.update(update_dict)
    return Config(**config_dict)


Config.__new__.__defaults__ = (None,) * len(Config._fields)

CONFIG_MAP = dict()

# Free style config
CONFIG_MAP['freestyle'] = Config(
    encoder_style=FreeStyle(GeneralParams(
        use_drum=False,
        sustain=False,
        max_length=1024,
        width=1024,
        height=1024,
        scale=80,
        shape='circle'
    )),
    style_params={
        'background_color': [1.0, 1.0, 1.0],
        'shape_colors': [
            (0.96, 0.0, 0.86),
            (0.82, 0.96, 0.02),
            (0.0, 1.0, 0.88),
            (0.0, 0.0, 0.0),
            (0.7, 0.0, 1.0)],
        'shapes': ['circle', 'rectangle']
    },
    input=None,
    output=None,
)
