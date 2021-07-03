# GPT2-Bulgarian Training-Tips-and-Tools
# Обучение на GPT2 модел на български - съвети и опит

GPT2 model training experience and tools for collecting or preparing datasets. 

Side notes:

wiki_... - Чрез скрипта за изтегляне... Не ми хареса раздробеното съдържание с огромен брой имена, употребени единично, имаше и грешки в извличането. По-добре ръчно на отделни избрани статии (но трудоемко) или чрез паяк или автоматизирано: Scrapy или собствен паяк или през Selenium с управление на четец (Chrome, Firefox) или по друг начин, ако ще се ползва Уикипедия.



**Discoveries:**

Check the GPU:
```
!nvidia-smi
Fri Jun 18 04:29:21 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 465.27       Driver Version: 460.32.03    CUDA Version: 11.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            Off  | 00000000:00:04.0 Off |                    0 |
| N/A   73C    P0    34W /  70W |  14218MiB / 15109MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
```

* It is possible to train **gpt2-medium** size transformer on Google Colab when you get a Tesla T4 with 16 GB (it shows 15). With the settings which I managed to run it occupies about 14 GB while training (13.88 GB) with config:

```
# Medium
num_heads = 16
configBIG = GPT2Config(
  vocab_size=tokenizerBIG.vocab_size,
  bos_token_id=tokenizerBIG.bos_token_id,
  eos_token_id=tokenizerBIG.eos_token_id,
  n_embd= 1024,
  n_head = num_heads,
  n_layer = 24
)

block_size = 100
BATCH_SIZE = num_heads 
BUFFER_SIZE = 5000 # 

Also with BUFFER_SIZE = 100 * num_heads (3600).
BUFFER_SIZE is for the dataset preparation.

'''
GPT2Config {
  "activation_function": "gelu_new",
  "architectures": [
    "GPT2LMHeadModel"
  ],
  "attn_pdrop": 0.1,
  "bos_token_id": 50251,
  "embd_pdrop": 0.1,
  "eos_token_id": 50250,
  "gradient_checkpointing": false,
  "initializer_range": 0.02,
  "layer_norm_epsilon": 1e-05,
  "model_type": "gpt2",
  "n_ctx": 1024,
  "n_embd": 1024,
  "n_head": 16,
  "n_inner": null,
  "n_layer": 24,
  "n_positions": 1024,
  "resid_pdrop": 0.1,
  "scale_attn_weights": true,
  "summary_activation": null,
  "summary_first_dropout": 0.1,
  "summary_proj_to_labels": true,
  "summary_type": "cls_index",
  "summary_use_proj": true,
  "transformers_version": "4.7.0",
  "use_cache": true,
  "vocab_size": 50255
}
```


The model required the batch size to be equal to the number of heads, otherwise it fails to fit the tensors.
For other configs see https://huggingface.co/transformers/v2.2.0/pretrained_models.html 

One error message, after debugging, also suggested that the size of the embedding vector should be divisible to the number of heads.
```
768/12 - SMALL
1024/16 - MEDIUM...
```

## Training ...

One epoch with the above settings over ~ 46.3 MB dataset in UTF8 with text mostly in cyrillic (2-bytes) ~ 18:35 min
Sample generation of a 200 token sequence, top_k = 40, temperature = 0.75, num_beams = 16 ... ~ 2:08 min ... 
Shorter context, lenght = 100, temperature = 1 ~ 0:42 

Save the model after each iteration/run of epochs.
Connect to your Google Drive and store it there in order to avoid losing data if you forget or be late to download the model. Also downloading with files.download() sometimes is very slow and during that time you're not using the GPU which may be penalized and the session to be interrupted automatically. 

I am not sure how much time is really allowed with a GPU and how much the actual usage of the GPU is weighed, but if you are using it consecutive days, it seemed it may get lower hours and the service may start denying to give you a GPU. Some say 12 h, maybe it depends on too many variables, time of the day, where you are located. At first it seemed about ~ 7-8 hours (also if not constant load), then it seemed it was fewer next days or it just denies. It is annoying that there are no warnings neither that an interrupt is approaching so to save your work or how long you're supposed to wait if rejected.

If you're on a session only with a CPU, I receive about 12.69 GB RAM and one core from an Intel Xeon E5-2696 v4 @ 2.20GHz
It may be enough for smaller models and small datasets for studying and debugging the process. That RAM is not enough even if the CPU was faster though.

```
Class: Server
Socket: FCLGA2011-3
Clockspeed: 2.2 GHz
Turbo Speed: 3.6 GHz
Cores: 22 Threads: 44
Typical TDP: 145 W
Other names: Intel(R) Xeon(R) CPU E5-2696 v4 @ 2.20GHz
CPU First Seen on Charts:  Q2 2016
CPUmark/$Price:  7.88     
Overall Rank:  151
Last Price Change:  $2,788.89 USD (2021-03-16)
Average CPU Mark
rating
21965
Single Thread Rating: 1950
Cross-Platform Rating: 68,469
Samples: 27*: (in my runs these days, 19.6.2021)
```
Sometimes the CPU is an older one:

```
Intel(R) Xeon(R) CPU @ 2.30GHz [Family 6 Model 63 Stepping 0]
```
From the 5-th generation Core.

Check it with: 

```
!cat /proc/cpuinfo

processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 79
model name	: Intel(R) Xeon(R) CPU @ 2.20GHz
stepping	: 0
microcode	: 0x1
cpu MHz		: 2199.998
cache size	: 56320 KB
physical id	: 0
siblings	: 2
core id		: 0
cpu cores	: 1
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 13
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm rdseed adx smap xsaveopt arat md_clear arch_capabilities
bugs		: cpu_meltdown spectre_v1 spectre_v2 spec_store_bypass l1tf mds swapgs taa
bogomips	: 4399.99
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:
```



