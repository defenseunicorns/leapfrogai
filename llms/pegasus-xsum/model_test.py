import unittest

from pegasus_xsum import PegasusXSum as Model

class PegasusXSum(unittest.TestCase):
    model = Model()
    def test_completion(self):
        output = self.model.complete(prompt="<|USER|>What's your mood today?<|ASSISTANT|>")
        print(output)

if __name__ == '__main__':
    unittest.main()