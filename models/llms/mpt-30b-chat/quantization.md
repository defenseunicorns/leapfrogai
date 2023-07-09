ct2-transformers-converter --model HuggingFaceH4/starchat-beta --revision main --quantization int8_float16 --output_dir starchatbeta_ct2_int8_float16

ct2-transformers-converter --model mosaicml/mpt-30b-chat --output_dir mpt-30b-chat_ct2 --quantization int8_float16 --trust_remote_code

ct2-transformers-converter --model HuggingFaceH4/starchat-beta --revision main --quantization float16 --output_dir starchatbeta_ct2
