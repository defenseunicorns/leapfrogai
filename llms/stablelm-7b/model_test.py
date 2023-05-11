import unittest

from stablelm3b import StableLM as Model



class TestStableLLM(unittest.TestCase):
    model = Model()
    def test_completion(self):
        output = self.model.complete(promt="<|USER|>What's your mood today?<|ASSISTANT|>")
        print(output)



if __name__ == '__main__':
    unittest.main()