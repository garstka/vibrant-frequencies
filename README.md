# vibrant-frequencies
Real-time sound visualization in Python.

Produces rapidly changing, colorful patterns from sound in real time.
You can find demos below.

## Epilepsy warning

Visualizations contain flashing lights.
Unsuitable for people with photosensitive epilepsy.

## Demos

Watch at 1080p60 for best effect.
 - [YouTube - Cinematic/Adventure music](https://www.youtube.com/watch?v=WfPJ8Lo08Oc&list=PL4OoIVecFjq7uyEJJ6B9BH0gSIEfM62iH&index=1)
 - [YouTube - Electronica](https://www.youtube.com/watch?v=aKeCkYlSRJU&index=2&list=PL4OoIVecFjq7uyEJJ6B9BH0gSIEfM62iH)
 - [YouTube - Dubstep](https://www.youtube.com/watch?v=hytzG58jVBE&list=PL4OoIVecFjq7uyEJJ6B9BH0gSIEfM62iH&index=3)

## Install

    pip3 install git+https://github.com/garstka/vibrant-frequencies

If this doesn't work on Linux, you may need to install additional
 dependencies. Here is more or less what I needed on Raspberry Pi:

    apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libportmidi-dev libsdl-ttf2.0-dev portaudio19-dev libffi-dev

## First run

Run using the command:

    vibrant-frequencies

Pick the input interface on first run. Demos were recorded using Stereo
Mix on Windows, but you can use a mic as well.
Settings are saved in `config.json`, you can edit them too.

To scale the visualization, use up/down arrow keys.

### Raspberry Pi 3

There are issues with performance on Raspberry Pi when running at 1080p.
You may need to reduce resolution to XVGA (1024x768) to achieve high enough FPS.

## Inspired by

 - [Building A Video Synthesizer in Python by Kirk Kaiser](https://www.makeartwithpython.com/blog/video-synthesizer-in-python/)
 - [17.11: Sound Visualization: Frequency Analysis with FFT - p5.js Sound Tutorial by The Coding Train](https://www.youtube.com/watch?v=2O3nm0Nvbi4)
 - [Audio Reactive LED Strip by Scott Lawson](https://github.com/scottlawsonbc/audio-reactive-led-strip)
 - A certain Media Player.

## To do

Besides improving code quality, adding more colors and visualizations:
 - Remove or adjust most of cookiecutter boilerplate.
 - Add autoscaling of visualizations.
 - Make initial run smarter, e.g. autodetection of native resolution.
 - Save more settings, such as visualization scale.
