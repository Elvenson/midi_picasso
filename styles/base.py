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

"""Base style class script."""

import logging
import magenta.music as mm

LOGGER = logging.getLogger(__name__)


class BaseStyle(object):    # pylint: disable=useless-object-inheritance
    """Base style class."""
    @staticmethod
    def _min_max_norm(value, old_min=1.0, old_max=127.0, new_min=0.0, new_max=1.0):
        """Min max normalizer."""
        return (value - old_min) / (old_max - old_min) * (new_max - new_min) + new_min

    def _read_midi(self, input_file):
        """
        Read midi file into note sequence.
        :param input_file: A string path to midi file.
        :return: Note sequence.
        """
        note_sequence = mm.midi_file_to_note_sequence(input_file)

        # Handle sustain pedal in primer.
        if self.config.sustain:
            note_sequence = mm.apply_sustain_control_changes(note_sequence)

        # Trim to desired number of seconds.
        if note_sequence.total_time > self.config.max_length:
            LOGGER.warning(
                'Note sequence %d is longer than max seconds %d, truncating.',
                note_sequence.total_time, self.config.max_length)
            note_sequence = mm.extract_subsequence(note_sequence, 0, self.config.max_length)

        # Whether or not remove drums.
        if any(note.is_drum for note in note_sequence.notes) and not self.config.use_drum:
            LOGGER.warning('Midi file contains drum sounds, removing.')
            notes = [note for note in note_sequence.notes if not note.is_drum]
            del note_sequence.notes[:]
            note_sequence.notes.extend(notes)

        # Set primer instrument and program.
        for note in note_sequence.notes:
            note.instrument = 1
            note.program = 0

        return note_sequence

    def encode_midi(self, input_file, output_file, params):
        """
        Encode midi into image.
        :param input_file: A string path to midi file.
        :param output_file: A string path to image file.
        :param params: A dictionary contains specific style parameters.
        :return:
        """
        raise NotImplementedError()

    def __init__(self, config=None):
        """
        Initializer base class.
        :param config: A GeneralParams object contains parameters.
        """
        if not config:
            raise ValueError('Required config.')

        self._config = config

    @property
    def config(self):
        """Get config."""
        return self._config
