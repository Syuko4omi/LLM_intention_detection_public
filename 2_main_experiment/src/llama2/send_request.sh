#!/bin/sh
#PJM -L rscgrp=share
#PJM -L gpu=4
#PJM -L elapse=12:00:00
#PJM -g gk77
#PJM -j

module load gcc/8.3.1
module load python/3.8.12
source venv/bin/activate
python3 -c "from huggingface_hub.hf_api import HfFolder; HfFolder.save_token('enter_token_here')"
huggingface-cli login --token enter_token_here
python3 send_request_to_llama2.py