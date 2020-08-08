# Midi Picasso: A Midi artistic visualization.

Midi Picasso converts midi file into artistic image. The idea is inspired by [Magenta Music Transformer
visualization](https://magenta.tensorflow.org/listen-to-transformer). Here is an example created with
`Chopin - Fantaisie-Impromptu (Op. 66)` midi file:
![Visualization](./data/example.png)

## Installation:
You need to install 2 main packages, the first one is `magenta` (for reading Midi file) the other is `pycairo` (for 
visualization). This repo requires `Python 3` version.

To install `magenta`, simply type:
```bash
pip install magenta==1.3.1
```

To install `pycairo`, type:
```bash
pip install pycairo==1.19.1
```

## How To Use:

To generate new image, you simply need to specify `input` (midi file path), `output` (generated image name) 
and style config (For now only `FreeStyle` class available). This repo provides one sample midi file for you 
to try:
```bash
python main.py --input=data/chopin_impromptu.mid --output=example.png --config=freestyle
```

***Note***: Each run will create new image since this style is based on randomness. Thus you can try to run many times 
and choose one that you prefer the most.