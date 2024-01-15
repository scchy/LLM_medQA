# python3
# Create Date: 2024-01-12
# Author: Scc_hy
# Func: web demo
# ==============================================================================
import gradio as gr
from dataclasses import asdict
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from appPrepare.interface import GenerationConfig, generate_interactive
from appPrepare.download_merge import dl_mg, logger
import os
import warnings
warnings.filterwarnings('ignore')

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.system(f'sh ./appPrepare/env_prepare.sh')
logger.info('1- Prepare Xtuner')
mg_path = dl_mg()
logger.info('2- Download and Merged Adapater & base mode')
generation_config = GenerationConfig(max_length=2048, top_p=0.01, temperature=0.01)
user_prompt = "<|User|>:{user}\n"
robot_prompt = "<|Bot|>:{robot}<eoa>\n"
cur_query_prompt = "<|User|>:{user}<eoh>\n<|Bot|>:"


def combine_history(prompt, chat_history):
    """
    chat_history [q, a]
    """
    total_prompt = ""
    for message in chat_history:
        cur_prompt = user_prompt.replace("{user}", message[0])
        itotal_prompt += cur_prompt
        cur_prompt = robot_prompt.replace("{robot}", message[1])
        itotal_prompt += cur_prompt
    total_prompt = total_prompt + cur_query_prompt.replace("{user}", prompt)
    return total_prompt


class Model_center():
    def __init__(self):
        # 构造函数，加载检索问答链
        self.model = (
            AutoModelForCausalLM.from_pretrained(mg_path, trust_remote_code=True)
            .to(torch.bfloat16)
            .cuda()
        )
        self.tokenizer = AutoTokenizer.from_pretrained(mg_path, trust_remote_code=True)

    def qa_answer(self, question: str, chat_history: list = []):
            if question == None or len(question) < 1:
                return "", chat_history
            try:
                real_prompt = combine_history(question, chat_history)
                out = ''
                for cur_response in generate_interactive(
                    model=self.model,
                    tokenizer=self.tokenizer,
                    prompt=real_prompt,
                    additional_eos_token_id=103028,
                    **asdict(generation_config),
                ):
                    out += cur_response

                chat_history.append((question, out))
                # 将问答结果直接附加到问答历史中，Gradio 会将其展示出来
                return "", chat_history
            except Exception as e:
                return e, chat_history



# 实例化核心功能对象
model_center = Model_center()
# 创建一个 Web 界面
block = gr.Blocks()
with block as demo:
    with gr.Row(equal_height=True):   
        with gr.Column(scale=15):
            # 展示的页面标题
            gr.Markdown("""<h1><center>InternLMDoctor</center></h1>
                <center>书生浦语-Doctor</center>
                """)
    with gr.Row():
        with gr.Column(scale=4):
            # 创建一个聊天机器人对象
            chatbot = gr.Chatbot(height=450, show_copy_button=True)
            # 创建一个文本框组件，用于输入 prompt。
            msg = gr.Textbox(label="Prompt/问题")

            with gr.Row():
                # 创建提交按钮。
                db_wo_his_btn = gr.Button("Chat")
            with gr.Row():
                # 创建一个清除按钮，用于清除聊天机器人组件的内容。
                clear = gr.ClearButton(
                    components=[chatbot], value="Clear console")
    
        db_wo_his_btn.click(model_center.qa_answer, inputs=[
                            msg, chatbot], outputs=[msg, chatbot])

    gr.Markdown("""提醒：<br>
    1. 初始化数据库时间可能较长，请耐心等待。
    2. 使用中如果出现异常，将会在文本输入框进行展示，请不要惊慌。 <br>
    """)


gr.close_all()
# 直接启动
demo.launch()
