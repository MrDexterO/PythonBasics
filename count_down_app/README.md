# Countdown Timer Application

This is a Python-based Countdown Timer application created using `tkinter` for the graphical user interface (GUI) and `pygame` for sound playback. The app allows users to set a countdown timer, and once the time reaches zero, it triggers an alarm sound. Users can start, pause, resume, and reset the timer, and the GUI will reflect the current countdown status.

## Features

- **Set Timer**: Users can input a duration in seconds and set the countdown timer.
- **Start/Pause/Resume**: Start or pause the countdown with the ability to resume the timer.
- **Reset Timer**: Reset the countdown to zero and allow a new time to be set.
- **Alarm Sound**: An alarm sound plays when the countdown reaches zero.
- **User Input Handling**: Input box with placeholder text that disappears when clicked and reappears when the input box loses focus.

## Requirements

- **Python 3.x**: The latest stable version of Python.
- **pygame**: A library used to handle audio playback (for the alarm sound).
- **tkinter**: A built-in Python library for building the GUI.

### Installing Dependencies

To run the application, you need to install Python 3.x and `pygame`. Follow the steps below to set up the application:

1. **Install Python 3.x**

   If you don't have Python installed, download it from the official [Python website](https://www.python.org/downloads/).

2. **Install pygame**

   You need to install the `pygame` library to handle audio playback. Run the following command in your terminal to install it:

   ```bash
   pip install pygame
