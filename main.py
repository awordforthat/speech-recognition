import asyncio
import functools

import speech_recognition as sr
import os


def parse_phrase(recognizer, audio):
    """
    Calls the specified backend with audio data and serializes the result.

    Args:
        recognizer: A Recognizer instance
        audio: The binary audio data to be analyzed.

    Returns:
        An object describing the result of the transcription.

    """
    assert isinstance(recognizer, sr.Recognizer)
    response = {"transcription": None, "success": False, "error": None}
    try:
        response["transcription"] = recognizer.recognize_google(audio)
        response["success"] = True
    except sr.RequestError as error:
        # API was unreachable or unresponsive
        response["error"] = f"Error: {error}"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    report(response)
    act(response)


def report(result):
    """
    Prints out the result of a transcription.

    Args:
        result: An object describing the results of the transcription.
    """
    if result.get("success"):
        print(f"You said: {result.get('transcription')}")
    else:
        print(f"Sorry, I didn't get that :(\nError: {result.get('error')}")


def act(result):
    """
    Given a successful response, attempts to find an action associated with
    the transcription. If one is found, calls the action method.

    Args:
        A result object with keys 'success' and 'transcription' (at a minimum)
    """
    if result.get("success"):
        phrase = result.get("transcription")
        action = phrase_actions.get(phrase)
        try:
            action()
        except:
            print(f"Phrase action '{phrase}' does not have an associated action")


def speak(phrase):
    """
    Prints the given string followed by an exclamation point.
    """
    print(f"{phrase}!")


phrase_actions = {
    "say hello": functools.partial(speak, "hello"),
    "say goodbye": functools.partial(speak, "goodbye"),
    "exit": functools.partial(os._exit, 0),
}

if __name__ == "__main__":
    # create audio tools
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=0)

    # mitigate background noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    # listen up!
    print("Speak!")
    recognizer.listen_in_background(microphone, parse_phrase)

    # keep listening forever
    asyncio.get_event_loop().run_forever()
