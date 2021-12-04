from __future__ import division

import re
import sys
import os
from google.cloud import speech
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/yushuyang/Documents/google cloud/speech-recognition-333708-ff061f2dba6b.json'
import pyaudio
from six.moves import queue
import time
import serial
import serial.tools.list_ports
import webbrowser
# Audio recording parameters

#begin voice recognition
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


#begin communicating from python to arduino
plist = list(serial.tools.list_ports.comports())
#from google.cloud import speech
if len(plist) <= 0:
    print("NO SERIAL PORT FOUND BB")
else:
    print("found one")
phrase = {"confident" : "intelligent"
        , "beautiful" : "smart"}
              
serialPort = "/dev/cu.usbmodem1301"  #串口，我的是COM3，这里你们要自己改
baudRate = 115200   #波特率

ser = serial.Serial(serialPort, baudRate, timeout = 0.5)

print("参数设置：串口=%s , 波特率=%d" % (serialPort, baudRate))



class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

def listen_print_loop(responses, keywords):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:

        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            x = transcript + overwrite_chars
            print(x)
            if any(keyword in x for keyword in keywords):
                # arr = bytes("python writes", 'utf-8')
                print("test")
                # to_ard = ser.write(arr)
                to_ard = ser.write('1'.encode('utf-8'))
            if any(keyword in x for keyword in keywords):
                # arr = bytes("python writes", 'utf-8')
                print("test")
                # to_ard = ser.write(arr)
                to_ard = ser.write('1'.encode('utf-8'))            
                
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0

def main():
    # Determine the list of keywords to be searched in the transcript
    #调整关键词
    keywords = ["smart", "powerful", "great"]
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "en-US"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses, keywords)

if __name__ == "__main__":
    main()

#end of voice recognition

#begin key words recognition
x = listen_print_loop(transcript, keywords)
print("x: ", x)
keywords = ["smart", "powerful", "great"]
keywords_2 = ["sad", "hello", "yes"]
if any(keyword in x for keyword in keywords):
    print("test")


# def callback(phr, phrase):
#     if phr == phrase["closeMainSystem"]:
#         """ speech.say("人机交互关闭，谢谢使用")
#         speech.stoplistening() """
#         sys.exit()
#     elif phr == phrase["weather"]:
#         print("exit")
        # speech.say("现在温度是" + str(sq) + "度")
        
# def comm_ardu(int):
#         sq = ser.readline()
#     sq = sq.strip()
#     print(str(time.time()) + "温度：" + str(sq))
#     arr = bytes("python writes", 'utf-8')
#     to_ard = ser.write(arr)


# while 1:
#     sq = ser.readline()
#     sq = sq.strip()
#     print(str(time.time()) + "温度：" + str(sq))
#     arr = bytes("python writes", 'utf-8')
#     to_ard = ser.write(arr)
#     # phr == speech.input()
#     #callback(phr, phrase)
#     # speech.say("You said %s" % phr)
#ser.close()