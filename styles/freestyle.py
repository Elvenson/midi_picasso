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

"""Free Style script."""
import random
import math
import cairo
from styles.base import BaseStyle    # pylint: disable=import-error


class FreeStyle(BaseStyle):
    """
    Free Style encoder, each note is a random shape positioned in random place,
    the size of the shape is determined by its note duration, the transparency
    is determined by note velocity.
    """
    def encode_midi(self, input_file, output_file, params):
        """Encodes midi into image."""
        note_sequence = self._read_midi(input_file)
        self._encode_ns(note_sequence, output_file, params)

    def _create_rectangle(self, duration, rgba):
        """
        Creates rectangle shape.
        :param duration: A float represents note duration.
        :param rgba: A tuple `(r, g, b, a)` represents RGBA color encode.
        :return:
        """
        # Random start point coordinate.
        x_coord = random.uniform(0, self.config.height / self._scale)
        y_coord = random.uniform(0, self.config.height / self._scale)

        # Find width and height of the rectangle.
        radian = random.uniform(math.pi / 8, math.pi / 4)
        width = math.cos(radian) * duration
        height = math.sin(radian) * duration

        # Rotate rectangle by random degree.
        rotate_deg = random.choice([-1, 1]) * random.uniform(0, 5) * math.pi / 180
        self._ctx.rotate(rotate_deg)
        self._ctx.rectangle(x_coord, y_coord, width, height)
        self._ctx.set_source_rgba(rgba[0], rgba[1], rgba[2], rgba[3])
        self._ctx.fill()

    def _create_circle(self, duration, rgba):
        """
        Creates circle shape.
        :param duration: A float represents note duration.
        :param rgba: A tuple `(r, g, b, a)` represents RGBA color encode.
        :return:
        """
        # Random start point coordinate.
        x_coord = random.uniform(0, self.config.height / self._scale)
        y_coord = random.uniform(0, self.config.height / self._scale)
        self._ctx.move_to(x_coord, y_coord)
        self._ctx.arc(x_coord, y_coord, duration, 0, math.pi * 2)
        self._ctx.close_path()
        self._ctx.set_source_rgba(rgba[0], rgba[1], rgba[2], rgba[3])
        self._ctx.fill()

    def _encode_ns(self, note_sequence, output_file, params):
        """
        Encodes note sequence into image.
        :param note_sequence: A note sequence from midi input.
        :param output_file: A string path to output file.
        :param params: A dictionary contains style parameters.
        :return:
        """
        # Add background color.
        self._ctx.rectangle(0, 0, self.config.width, self.config.height)
        self._ctx.set_source_rgb(*params['background_color'])
        self._ctx.fill()
        for note in note_sequence.notes:
            color = random.choice(params['shape_colors'])

            # Add alpha.
            alpha = self._min_max_norm(note.velocity)
            rgba = (color[0], color[1], color[2], alpha)

            # Random shape.
            shape = random.choice(params['shapes'])
            if shape == 'rectangle':
                self._create_rectangle(note.end_time - note.start_time, rgba)
            elif shape == 'circle':
                self._create_circle(note.end_time - note.start_time, rgba)
            else:
                raise ValueError('Cannot recognize shape {}'.format(shape))

        # Write image to file.
        self._surface.write_to_png(output_file)

    def __str__(self):
        return 'FreeStyle class with config {}'.format(self.config)

    def __init__(self, config=None):
        super().__init__(config)
        self._surface = cairo.ImageSurface(     # pylint: disable=no-member
            cairo.FORMAT_ARGB32, config.width, config.height)    # pylint: disable=no-member
        self._ctx = cairo.Context(self._surface)    # pylint: disable=no-member

        # Set scale.
        if config.scale and config.scale <= 0:
            raise ValueError('Scale value must be larger than 0')
        self._ctx.scale(config.scale, config.scale)
        self._scale = config.scale
