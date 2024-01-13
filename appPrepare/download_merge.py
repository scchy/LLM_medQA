import os
from openxlab.model import download as ox_download
from modelscope.hub.snapshot_download import snapshot_download
from transformers.utils import logging
import json
import openxlab

key_dict = {
    "ak" : "yzqrvr9mx3goqpgraejj ",
    "sk" : "67pbdwkjvyl23q89zv2xrlgbr91nzramjmwazrye"
}


openxlab.login(ak=key_dict['ak'], sk=key_dict['sk'])
logger = logging.get_logger(__name__)


def dl_mg():
    # hf modelscope download 
    hf_path = "/home/xlab-app-center/hf"
    if not os.path.exists(hf_path):
        snapshot_download(model_id='sccHyFuture/LLM_medQA_adapter', cache_dir=hf_path, revision='v1.0.1')
    
    logger.info(f'[ dl_mg ] adapter --> {hf_path}')
    # InternLM-chat-7b
    lm_7b_path = "/home/xlab-app-center/InternLM-chat-7b"
    if not os.path.exists(lm_7b_path):
        ox_download(model_repo='OpenLMLab/InternLM-chat-7b', output=lm_7b_path)

    logger.info(f'[ dl_mg ] InternLM-chat-7b --> {lm_7b_path}')
    mg_path = "/home/xlab-app-center/hf_merged"
    if not os.path.exists(mg_path):
        os.system(f'mkdir -p {mg_path}')

    os.system(f"xtuner convert merge {lm_7b_path} {hf_path} {mg_path}")
    logger.info(f'[ dl_mg ] xtuner convert merge --> {mg_path}')
    return  mg_path

