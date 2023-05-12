import unittest

from stablelm3b import StableLM as Model

import torch


class TestStableLLM(unittest.TestCase):
    model = Model()

    
    def test_completion(self):
        output = self.model.complete(prompt="<|USER|>What's your mood today?<|ASSISTANT|>")
        # print(output)

    def test_memory(self):
        self.print_memory()
        for i in range(1,10):
            self.test_completion()
        self.print_memory()
        self.free()
        self.print_memory()

    def print_memory(self):
        print("torch.cuda.memory_allocated: %fGB"%(torch.cuda.memory_allocated(0)/1024/1024/1024))
        print("torch.cuda.memory_reserved: %fGB"%(torch.cuda.memory_reserved(0)/1024/1024/1024))
        print("torch.cuda.max_memory_reserved: %fGB"%(torch.cuda.max_memory_reserved(0)/1024/1024/1024))

    def free(self):
        torch.cuda.empty_cache()

if __name__ == '__main__':
    unittest.main()