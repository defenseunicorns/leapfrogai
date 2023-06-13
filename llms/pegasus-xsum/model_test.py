import unittest
import logging

from pegasus_xsum import PegasusXSum as Model

class PegasusXSum(unittest.TestCase):
    model = Model()
    
    def test_completion(self):
        prompt="Defense Unicorns provides secure, open source and infrastructure agnostic applications and tools that enable our partners to rapidly accelerate their software acquisition and delivery processes. Our open source applications enable DevSecOps on even the most secure systems. We are innovators, software engineers, and veterans with decades of experience delivering technology programs across the DoD as well as the broader federal market. Our team of unicorns are zany and passionate individuals who are dedicated to mission success."

        logging.info(f"Prompt: {prompt} \n")

        response = self.model.complete(prompt)

        logging.info(f"Response: {response} \n")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()