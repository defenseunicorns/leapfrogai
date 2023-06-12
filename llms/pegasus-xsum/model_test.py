import unittest

from pegasus_xsum import PegasusXSum as Model

class PegasusXSum(unittest.TestCase):
    model = Model()
    def test_completion(self):
        output = self.model.complete(prompt=" Who are you? We are the Brigade of Fatherly Volunteers. We are looking for comrades. What kind of brigade is this? We are from the Rehobovskys. Ah, I heard you. Jewish bandits? We are discussing this with your commander. Do not make it complicated. Whistles Let's go. Whistanwe whistles Shouting Shouting Viktor Panchenko, commander of the October Triad. We are being complained about. That the Jewish gang is robbing the peaceful population that supports us. I am waiting for an explanation. When you are going to the people, you are trying to help the people to the front. And we mean to steal. We are soldiers of the Red Army. Well, we have the most common enemy. And in our socialist homeland, everyone is treated without prejudice. We are not Jews. But the Jews are not fighting. The Latvians are fighting. Well, we will see. Select your best fighters and send them. What is the honor?")
        print(output)

if __name__ == '__main__':
    unittest.main()