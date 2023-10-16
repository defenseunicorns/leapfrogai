import unittest
import uuid

from main import Whisper
import leapfrogai
import concurrent.futures

# Helper functions
def whisper_transcribe(whisper):
    current_task_num = uuid.uuid4()

    # Load the audio file into bytes
    with open("tests/data/0min12sec.wav", "rb") as audio_file:
        audio_data = audio_file.read()

    # Initialize the AudioRequest with the loaded audio data
    audio_request = leapfrogai.AudioRequest(chunk_data=audio_data)

    # Load the entire file as a single AudioRequest
    audio_requests: list[leapfrogai.AudioRequest] = [audio_request]

    print(f'Beginning task {current_task_num}')
    result = whisper.Transcribe(audio_requests, None)
    print(f'Ending task {current_task_num}')
    return result

class TestParallelization(unittest.IsolatedAsyncioTestCase):

    async def test_parallel_upload(self):
        whisper = Whisper()

        expected_transcription = ''
        with open("tests/data/0min12sec.txt", "rb") as text_file:
            expected_transcription = text_file.read().decode()

        # Attempt to transcribe this file multiple times in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(whisper_transcribe, whisper)
            future2 = executor.submit(whisper_transcribe, whisper)

            self.assertEqual(future1.result().text.strip(), expected_transcription)
            self.assertEqual(future2.result().text.strip(), expected_transcription)

if __name__ == '__main__':
    unittest.util._MAX_LENGTH = 300
    unittest.main()
