import argparse
import asyncio
import functools

import speech_recognition as sr


def get_backend(name, recognizer):
    """
    Returns a recognizer function for the given backend name.

    Args:
        name: The string name of a backend.
        recognizer: a Recognizer instance to call the backend.

    Returns:
        A recognizer function that takes an Audio Source as its only parameter.

    Raises:
        NotImplementedError: Raises this if the backend is not recognized.
    """
    assert isinstance(recognizer, sr.Recognizer)
    if name == "google":
        return recognizer.recognize_google
    elif name == "cmu":
        return recognizer.recognize_sphinx
    else:
        raise NotImplementedError(f"Backend {name} not set up yet!")


def parse_phrase(recognizer, audio, backend):
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
        response["success"] = True
        response["transcription"] = get_backend(backend, recognizer)(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    report(response)


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


if __name__ == "__main__":
    # configure our setup
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "backend",
        choices=("google", "cmu"),
        nargs="?",
        default="google",
        help="The name of the backend to use (one of 'google' or 'cmu')",
    )
    args = parser.parse_args()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=0)

    # mitigate background noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    # listen up!
    print("Speak!")
    stop_callback = recognizer.listen_in_background(
        microphone, functools.partial(parse_phrase, backend=args.backend)
    )

    # unnecessary async to keep listening forever
    asyncio.get_event_loop().run_forever()
