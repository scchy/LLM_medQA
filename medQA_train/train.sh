#!/bin/sh


CUR=$(dirname $0)
cd $CUR

sh env_prepare.sh
conda activate LLM
python internlm_chat_7b_qlora_medqa2019_e3.py
# 开始微调
xtuner train internlm_chat_7b_qlora_medqa2019_e3.py --deepspeed deepspeed_zero2 > __ds_xtuner.log


