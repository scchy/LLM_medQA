#!/bin/sh

path_dir=/home/scc/sccWork/myGitHub/LLM_medQA
cd ${path_dir}

mkdir xtuner019 && cd xtuner019
git clone -b v0.1.9  https://github.com/InternLM/xtuner
cd xtuner
pip install -e '.[all]'
mkdir ${path_dir}/ft-medqa && cd ${path_dir}/ft-medqa 

# 模型下载
mkdir ${path_dir}/ft-medqa/internlm-chat-7b
pip install modelscope
cd ${path_dir}/ft-medqa
apt install git git-lfs -y
git lfs install
git lfs clone https://modelscope.cn/Shanghai_AI_Laboratory/internlm-chat-7b.git -b v1.0.3

# 数据下载
git clone https://github.com/abachaa/Medication_QA_MedInfo2019
cd Medication_QA_MedInfo2019 && \
mv MedInfo2019-QA-Medications.xlsx ../ && \
cd ..

pip install openpyxl


# 复制配置文件到当前目录
# xtuner copy-cfg internlm_chat_7b_qlora_oasst1_e3 .
