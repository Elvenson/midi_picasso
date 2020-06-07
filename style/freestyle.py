from style.base import BaseStyle
import random
import cairo
import math

SHAPE_COLOR = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
SHAPES = ['rectangle', 'circle']


class FreeStyle(BaseStyle):
	def encode_midi(self):
		ns = self._read_midi()
		self._encode_ns(ns)
		self.surface.write_to_png(self.output)

	@staticmethod
	def _min_max_norm(x, old_min=1, old_max=127, new_min=0.0, new_max=1.0):
		return (x - old_min) / (old_max - old_min) * (new_max - new_min) + new_min

	def _create_rectangle(self, duration, rgba):
		# Random start point coordinate
		x = random.uniform(0, self.height / self._scale)
		y = random.uniform(0, self.height / self._scale)

		# Find width and height of the rectangle
		radian = random.uniform(math.pi / 8, math.pi / 4)
		width = math.cos(radian) * duration
		height = math.sin(radian) * duration

		# Rotate rectangle by random degree
		rotate_deg = random.choice([-1, 1]) * random.uniform(0, 5) * math.pi / 180
		self.context.rotate(rotate_deg)
		self.context.rectangle(x, y, width, height)
		self.context.set_source_rgba(rgba[0], rgba[1], rgba[2], rgba[3])
		self.context.fill()

	def _create_circle(self, duration, rgba):
		# Random start point coordinate
		x = random.uniform(0, self.height / self._scale)
		y = random.uniform(0, self.height / self._scale)

		self.context.move_to(x, y)
		self.context.arc(x, y, duration, 0, math.pi * 2)
		self.context.close_path()
		self.context.set_source_rgba(rgba[0], rgba[1], rgba[2], rgba[3])
		self.context.fill()

	def _encode_ns(self, ns):
		for index, note in enumerate(ns.notes):
			color = random.choice(SHAPE_COLOR)

			# Add alpha
			alpha = self._min_max_norm(note.velocity)
			rgba = (color[0], color[1], color[2], alpha)

			# Random shape
			shape = random.choice(
				SHAPES)
			if shape == 'rectangle':
				self._create_rectangle(note.end_time - note.start_time, rgba)
			elif shape == 'circle':
				self._create_circle(note.end_time - note.start_time, rgba)
			else:
				raise ValueError('Cannot recognize shape {}'.format(shape))

	def __init__(self, filename, output, use_drum=False, sustain=False, max_length=1024, width=512, height=512, scale=200):
		super().__init__(filename, output, use_drum, sustain, max_length, width, height)
		self._surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
		self._ctx = cairo.Context(self.surface)

		# Add white background color
		self._ctx.rectangle(0, 0, width, height)
		self._ctx.set_source_rgb(0.9, 0.9, 0.9)
		self._ctx.fill()

		# Set scale
		if scale <= 0:
			raise ValueError('Scale value must be larger than 0')
		self._ctx.scale(scale, scale)
		self._scale = scale

	@property
	def context(self):
		return self._ctx

	@property
	def surface(self):
		return self._surface
