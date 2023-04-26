dummy_models = [
    {
        "data": [
            {
                "id": "model-id-0",
                "object": "model",
                "owned_by": "organization-owner",
                "permission": [],
            },
            {
                "id": "model-id-1",
                "object": "model",
                "owned_by": "organization-owner",
                "permission": [],
            },
            {"id": "model-id-2", "object": "model", "owned_by": "openai", "permission": []},
        ],
        "object": "list",
    }
]

dummy_model = {
    "id": "model-id-0",
    "object": "model",
    "owned_by": "organization-owner",
    "permission": [],
}

dummy_engine = {"prompt": "Say hello world three times", "temperature": 0.6}


dummy_complete = {
    "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
    "object": "text_completion",
    "created": 1589478378,
    "model": "text-davinci-003",
    "choices": [
        {
            "text": "\n\nThis is indeed a test",
            "index": 0,
            "logprobs": None,
            "finish_reason": "length",
        }
    ],
    "usage": {"prompt_tokens": 5, "completion_tokens": 7, "total_tokens": 12},
}

dummy_chat = {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "\n\nHello there, how may I assist you today?",
            },
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21},
}

dummy_edit = {
    "object": "edit",
    "created": 1589478378,
    "choices": [
        {
            "text": "What day of the week is it?",
            "index": 0,
        }
    ],
    "usage": {"prompt_tokens": 25, "completion_tokens": 32, "total_tokens": 57},
}

dummy_embedding = {
    "object": "list",
    "data": [
        {
            "object": "embedding",
            "embedding": [
                0.0023064255,
                -0.009327292,
                -0.0028842222,
            ],
            "index": 0,
        }
    ],
    "model": "text-embedding-ada-002",
    "usage": {"prompt_tokens": 8, "total_tokens": 8},
}

dummy_engine = {
    "encoding_format": "base64",
    "input": [
        [38136, 309, 30173, 11, 9671, 309, 23270, 4900, 11, 1057, 5629, 21270, 323, 10657, 74569, 1543, 13, 17384, 315, 8151, 323, 279, 34046, 13, 4702, 1238, 315, 279, 13814, 7301, 13, 3092, 12637, 9053, 13, 262, 8155, 1060, 20562, 12, 777, 8774, 603, 10980, 13, 1115, 1060, 584, 527, 5616, 3871, 1578, 13], [5966, 1060, 20562, 12, 777, 8774, 603, 10980, 13, 1115, 1060, 584, 527, 5616, 3871, 1578, 13, 256, 55314, 11, 584, 3449, 439, 12643, 13063, 323, 17565, 812, 13, 2030, 1455, 23659, 439, 9053, 13, 256, 3161, 264, 14523, 311, 832, 2500, 311, 279, 3778, 1274, 311, 279, 18039, 13], [90243, 11, 584, 3449, 439, 12643, 13063, 323, 17565, 812, 13, 2030, 1455, 23659, 439, 9053, 13, 256, 3161, 264, 14523, 311, 832, 2500, 311, 279, 3778, 1274, 311, 279, 18039, 13, 256, 1628, 449, 459, 15375, 402, 4776, 9006, 430, 11542, 690, 2744, 38586, 927, 78001, 13], [3112, 449, 459, 15375, 402, 4776, 9006, 430, 11542, 690, 2744, 38586, 927, 78001, 13, 256, 19198, 2919, 4227, 11, 8524, 753, 36011, 21810, 16495, 311, 27116, 279, 41582, 315, 279, 1949, 1917, 7422, 568, 1436, 1304, 433, 37920, 311, 813, 95072, 5627, 13, 2030, 568, 25587, 296, 16164, 50904, 13], [42560, 2919, 4227, 11, 8524, 753, 36011, 21810, 16495, 311, 27116, 279, 41582, 315, 279, 1949, 1917, 7422, 568, 1436, 1304, 433, 37920, 311, 813, 95072, 5627, 13, 2030, 568, 25587, 296, 16164, 50904, 13, 256, 1283, 3463, 568, 1436, 6638, 1139, 19278, 323, 279, 1917, 1053, 6638, 927, 13, 12361, 568, 2322, 264, 7147, 315, 8333, 568, 2646, 35706, 13]
    ]
}

dummy_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
