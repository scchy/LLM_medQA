#!/bin/sh

mkdir hf
export MKL_SERVICE_FORCE_INTEL=1

# Adapter
xtuner convert pth_to_hf \
    ./internlm_chat_7b_qlora_medqa2019_e3.py \
    ./work_dirs/internlm_chat_7b_qlora_medqa2019_e3/epoch_3.pth \
    ./hf