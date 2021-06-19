# gpt-2-training-tools

GPT2 model training experience and tools for collecting or preparing datasets. 

Discoveries:

-- It is possible to train gpt2-medium size transformer on Google Colab when you get a Tesla T4 with 16 GB (it shows 15). With the settings which I managed to run it occupies about 14 GB while training (13.88 GB) with config:
```
# MEDIUM
num_heads = 16
configBIG = GPT2Config(
  vocab_size=tokenizerBIG.vocab_size,
  bos_token_id=tokenizerBIG.bos_token_id,
  eos_token_id=tokenizerBIG.eos_token_id,
  n_embd= 1024,
  n_head = num_heads,
  n_layer = 24 #num_layers #24 #24
)

block_size = 100
BATCH_SIZE = num_heads 
BUFFER_SIZE = 5000 # 
```
The model required the batch size to be equal to the number of heads, otherwise it fails to fit the tensors.
For other configs see https://huggingface.co/transformers/v2.2.0/pretrained_models.html 

