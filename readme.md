# 2020 Sound
### An audio time-of-arrival alignment system
Finlay Braithwaite, OCAD University
## Introduction
As the focus of my master’s education in Digital Futures at OCAD, I will develop a prototype for a **positionally-aware microphone and DSP alignment system**. This system would allow for automatic alignment of multiple microphone perspectives to sound sources.
## Production Methods
## Sync Reference
In production, the distance of sound sources and microphones relative to one another would be measured. My research will explore modulating a high resolution longitudinal timecode reference in the ultrasonic frequency domain, providing a platform to document relative TOAs from multiple sources at multiple microphones.
### Capturing Metadata
The high-resolution positional reference generated and captured in production is then translated into metadata, embedded with or near the correlating audio information; the standard audio recording. Maintaining synchronization of this metadata to the recorded audio is of paramount importance.
## Postproduction
The usefulness of this captured positional reference data is that it allows us to line up microphones in the post production process.
### DSP Varispeed
* The unpacked metadata feeds a digital signal processor (DSP) offset and varispeed engine.
 * The processor aligns multiple perspectives to a sound source. 
   * Offset is applied to align perspectives at the start of the metadata.
   * The varispeed process corrects for changes to the relative positions during the recording.
     * For example, if a microphone moved closer to a source during the recording, the varispeed process would retard the audio to effectively nullify the movement.
## Background
The transduction of physical, acoustic sound at multiple perspectives is rife with problems. Yet this technique forms the backbone of the current audio production paradigm. A guitar captured with three microphones, a drum kit captured with over a dozen microphones are musical examples of this approach. In film production, an actor in a scene wears a lavalier microphone, is captured by a planted microphone, and is tracked by a boom operator. Multiple microphone perspectives allow us to balance, shape, and emphasize different aspects of a source. However, each perspective we add is located at a varying distance. Factoring the speed of sound against this distance leaves us with a varying time-of-arrival at each microphone. A source strikes the closest microphone first, the furthest last. Blending these misaligned images can cause as much good as bad. Frequencies across the spectrum are emphasized and deemphasized in a process known as comb filtering.
![Time/Distance Relationship Between Source and Microphones](http://webspace.ocad.ca/~3164558/TempLibrary/TimeDistance.svg)
_Time/Distance Relationship Between Source and Microphones_

Distance (metres) | Time (ms)
----------------- | ------------------
__0.01__ | _0.03_
__0.10__ | _0.29_
__0.50__ | _1.46_
__1.00__ | _2.92_
_Distance plotted against time of arrival, a factor of the **speed of sound** (343 m/s)._
## Objectives
In the process of obtaining my master’s degree, I would endeavour to create a working prototype of this system. Leading up to this, I would develop the framework upon which the prototype would be based. Over the years I have developed an advanced appreciation of the issue and have applied numerous strategies to address the problem in my own productions. It is through fulfilling the experience of completing my master’s degree in Digital Futures, that I would gain the knowledge and resources to develop a prototype.

Markdown written in terminal using Pico. SVG created in Adobe Illustrator.
