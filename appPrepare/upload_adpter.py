# 1- 执行目录 /root/ft-medqa
# 2- 创建 configuration.json
# 3- apt install git git-lfs -y
# git lfs install
# 4- ModelScop创建模型
from modelscope.hub.api import HubApi

# 请从ModelScope个人中心->访问令牌获取'
YOUR_ACCESS_TOKEN = 'xxx'

api = HubApi()
api.login(YOUR_ACCESS_TOKEN)
api.push_model(
    model_id="sccHyFuture/LLM_medQA_adapter", 
    model_dir="./hf"
)