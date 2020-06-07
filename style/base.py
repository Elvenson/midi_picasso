import magenta.music as mm
import logging

LOGGER = logging.getLogger(__name__)


class BaseStyle(object):
	def _read_midi(self):
		ns = mm.midi_file_to_note_sequence(self._filename)

		# Handle sustain pedal in primer.
		if self._sustain:
			ns = mm.apply_sustain_control_changes(ns)

		# Trim to desired number of seconds.
		if ns.total_time > self._max_length:
			LOGGER.warning('Note sequence %d is longer than max seconds %d, truncating.' % (ns.toal_time, self._max_length))
			ns = mm.extract_subsequence(ns, 0, self._max_length)

		# Whether or not remove drums.
		if any(note.is_drum for note in ns.notes) and not self._use_drum:
			LOGGER.warning('Midi file contains drum sounds, removing.')
			notes = [note for note in ns.notes if not note.is_drum]
			del ns.notes[:]
			ns.notes.extend(notes)

		# Set primer instrument and program.
		for note in ns.notes:
			note.instrument = 1
			note.program = 0

		return ns

	def encode_midi(self):
		raise NotImplementedError()

	def __init__(self, filename, output, use_drum=False, sustain=False, max_length=1024, width=512, height=512):
		self._use_drum = use_drum
		self._sustain = sustain
		self._max_length = max_length
		self._filename = filename
		self._output = output
		self._width = width
		self._height = height

	@property
	def width(self):
		return self._width

	@property
	def height(self):
		return self._height

	@property
	def output(self):
		return self._output

