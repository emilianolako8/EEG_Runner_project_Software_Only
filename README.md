# EEG_Runner_project_Software_Only
EEG-Controlled Runner Game (Software Simulation)

A real-time Brain-Computer Interface (BCI) simulation project that connects synthetic EEG signals to an interactive runner game.

This project simulates realistic EEG brainwave data (alpha rhythms, noise, and blink artifacts) and visualizes it live using PyQtGraph, while a Pygame runner game reacts to detected blink spikes.

Clicking the BLINK button injects a spike into the EEG signal, which appears in the waveform and triggers the player to jump — mimicking how a real EEG-based BCI system would work.

## Features

Real-time EEG signal simulation (256 Hz)

Alpha, theta, beta wave components

Blink artifact injection

Live EEG visualization (PyQtGraph)

Pygame runner game controlled by EEG events

Multi-process architecture (simulates real acquisition pipeline)

Event-driven game interaction

## Architecture

The system is divided into three processes:

EEG Simulator
Generates synthetic brainwave signals and blink spikes.

Signal Visualization (PyQtGraph)
Displays a scrolling real-time EEG waveform.

Game Engine (Pygame)
Listens for blink events and triggers player jumps.

Communication is handled using multiprocessing.Queue, simulating real hardware data streaming.

## How It Works

The simulator generates continuous EEG-like signals.

When the BLINK button is pressed:

A spike is injected into the signal.

A blink event is broadcast.

The game receives the event and makes the player jump.

The spike is visible in the EEG plot window.

## Technologies Used

Python

Pygame

PyQtGraph

Multiprocessing

NumPy (signal math)

## Why This Project?

This project demonstrates core Brain-Computer Interface concepts without requiring physical EEG hardware. It replicates a real-time acquisition → processing → visualization → control pipeline entirely in software.

It’s a strong foundation for:

Neurofeedback systems

BCI research prototypes

EEG-based gaming

Real hardware integration (future extension)
