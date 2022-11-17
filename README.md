# Speech Recognition Demo
Code to accompany Boston Python presentation on speech recognition

Accompanying slides here: https://docs.google.com/presentation/d/1Y9Bu2fKr3iGeSKtkIercm_x7fGV9DrGU8ul1X4Ppa0c/edit?usp=sharing

This script demonstrates the use of the [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library to listen to an audio device, parse keywords out of the stream, and act on them. 

## Installation
1. Create a virtual environment with `python -m venv <your venv name>`
2. Activate the virtual environment: `call <venv name>\Scripts\activate` (Windows) or `source <venv name>/bin/activate` (OSX/Linux)
3. Install the requirements: `pip install -r requirements.txt`. If you would like to contribute to this repo, you should also install the packages in `dev_requirements.txt`

## Running the project
From the root of the project, run `python main.py`. If you have a microphone connected, you should see a prompt on the command line to say something. When you do, you'll see output according to what the computer thinks you've said.

## Current phrases:
| Phrase | Action |
| ------ | ------ |
| "say hello" | Prints "Hello!" to the console |
| "say goodbye" | Prints "Goodbye!" to the console |
| "exit" | Exits the program |

## Things to note
- This uses the free [Google Web Speech API](https://wicg.github.io/speech-api/) with the default API key that ships with the Speech Recognition library. It is severely rate limited, and is guaranteed only by the goodness of Google's heart. It may not work in the future!
- The exit command on Windows is really hacky. Don't use it as an example for important code.
