import logging
import argparse
from style.freestyle import FreeStyle


LOGGER = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'


def parse_arg():
	parser = argparse.ArgumentParser()

	# Input argument
	parser.add_argument(
		'--verbosity',
		choices=[
			'DEBUG',
			'ERROR',
			'FATAL',
			'INFO',
			'WARN'
		],
		default='INFO',
		help='Set logging verbosity'
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
	encoder_style = FreeStyle(filename=params.input, output=params.output)
	encoder_style.encode_midi()


if __name__ == '__main__':
	args = parse_arg()
	logging.basicConfig(level=getattr(logging, args.verbosity), format=LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
	run(args)
