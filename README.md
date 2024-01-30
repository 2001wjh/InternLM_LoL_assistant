# LOL智能小助手

**OpenXLab 体验地址：	**

> *此仓库主要用于将 LOL智能小助手项目部署到 OpenXLab 或 ModelScope 。*

## 介绍

&emsp;&emsp;LOL智能小助手是利用op.gg上的部分数据，与B站中的视频攻略，基于[InternLM](https://github.com/InternLM/InternLM.git)进行LoRA微调与RAG完成的LOL智能小助手问答demo。

> 

&emsp;&emsp;

> 具体如何实现全流程的 Character-AI 微调，可参考主仓库-[huanhuan-chat](https://github.com/KMnO4-zx/huanhuan-chat.git)。
>
> 如何学习大模型部署和微调请参考：[开源大模型食用指南](https://github.com/datawhalechina/self-llm.git) 以及 [书生·浦语大模型实战营课程](https://github.com/InternLM/tutorial.git)

&emsp;&emsp;***欢迎大家来给[InternLM2](https://github.com/InternLM/InternLM.git)，点点star哦~***



## 数据集

&emsp;&emsp;lol智能小助手 数据集采用OPGG的胜率、出场率、弱势英雄、当前版本的level等组成200余条，将每条数据完成扩充后，共计【11400】余条，用扩充后的数据集完成LORA微调，数据集样例：

```text

```

​		可以使用仓库中的脚本【】完成opgg的爬取，并使用脚本【】完成数据集的扩充。

## RAG

​		RAG就是通过检索获取相关的知识并将其融入Prompt，让大模型能够参考相应的知识从而给出合理回答。因此，可以将RAG的核心理解为“检索+生成”，前者主要是利用向量数据库的高效存储和检索能力，召回目标知识；后者则是利用大模型和Prompt工程，将召回的知识合理利用，生成目标答案。

完整的RAG应用流程主要包含两个阶段：

- 数据准备阶段：数据提取——>文本分割——>向量化（embedding）——>数据入库

- 应用阶段：用户提问——>数据检索（召回）——>注入Prompt——>LLM生成答案

  LOL智能小助手使用的是从B站攻略视频中生成的攻略文字，字数逾10w+，完成知识库构建。使用到开源词向量模型 Sentence Transformer完成embedding，借助开源第三方库NLTK完成tokenize和tagger。使用 LangChain 提供的 FileLoader 对象来加载目标文件，得到由目标文件解析出的纯文本内容。

## 微调

&emsp;&emsp;有两种方案，我更倾向于使用 XTuner 训练， XTuner 有各个模型的一键训练脚本，很方便。且对 InternLM2 的支持度最高。

### 方案一：Transformers 

&emsp;&emsp;使用 Transformers 的 Trainer 进行微调，具体脚本可参考[internlm2-chat-lora](./train/internlm2-chat-lora.ipynb)，该脚本在`train`文件夹下。脚本内有较为详细的注释。

### 方案二：XTuner

&emsp;&emsp;使用 XTuner 进行微调，具体脚本可参考[internlm2_chat_7b_qlora_oasst1_e3_copy.py](./train/internlm2_chat_7b_qlora_oasst1_e3_copy.py)，该脚本在`train`文件夹下。脚本内有较为详细的注释。

## OpenXLab 部署 lol智能小助手

&emsp;&emsp;仅需要 Fork 本仓库，然后在 OpenXLab 上创建一个新的项目，将 Fork 的仓库与新建的项目关联，即可在 OpenXLab 上部署 Chat-嬛嬛。

&emsp;&emsp;***OPenXLab lol智能小助手***

![Alt text](images/openxlab.png)

## LmDeploy部署

- 首先安装LmDeploy

```shell
pip install -U lmdeploy
```

- 然后转换模型为`turbomind`格式

> --dst-path: 可以指定转换后的模型存储位置。

```shell
lmdeploy convert internlm2-chat-7b  要转化的模型地址 --dst-path 转换后的模型地址
```

- LmDeploy Chat 对话

```shell
lmdeploy chat turbomind 转换后的turbomind模型地址
```

## OpneCompass 评测

- 安装 OpenCompass

```shell
git clone https://github.com/open-compass/opencompass
cd opencompass
pip install -e .
```

- 下载解压数据集

```shell
cp /share/temp/datasets/OpenCompassData-core-20231110.zip /root/opencompass/
unzip OpenCompassData-core-20231110.zip
```

- 评测启动！

```shell
python run.py \
    --datasets ceval_gen \
    --hf-path /root/model/huanhuan/kmno4zx/huanhuan-chat-internlm2 \
    --tokenizer-path /root/model/huanhuan/kmno4zx/huanhuan-chat-internlm2 \
    --tokenizer-kwargs padding_side='left' truncation='left'     trust_remote_code=True \
    --model-kwargs device_map='auto' trust_remote_code=True \
    --max-seq-len 2048 \
    --max-out-len 16 \
    --batch-size 2  \
    --num-gpus 1 \
    --debug
```

## Lmdeploy&opencompass 量化以及量化评测  

### `W4`量化评测  

- `W4`量化

```shell
lmdeploy lite auto_awq 要量化的模型地址 --work-dir 量化后的模型地址
```

- 转化为`TurbMind`

```shell
lmdeploy convert internlm2-chat-7b 量化后的模型地址  --model-format awq --group-size 128 --dst-path 转换后的模型地址
```

- 评测`config`编写  

```python
from mmengine.config import read_base
from opencompass.models.turbomind import TurboMindModel

with read_base():
 # choose a list of datasets   
 from .datasets.ceval.ceval_gen import ceval_datasets 
 # and output the results in a choosen format
#  from .summarizers.medium import summarizer

datasets = [*ceval_datasets]

internlm2_chat_7b = dict(
     type=TurboMindModel,
     abbr='internlm2-chat-7b-turbomind',
     path='转换后的模型地址',
     engine_config=dict(session_len=512,
         max_batch_size=2,
         rope_scaling_factor=1.0),
     gen_config=dict(top_k=1,
         top_p=0.8,
         temperature=1.0,
         max_new_tokens=100),
     max_out_len=100,
     max_seq_len=512,
     batch_size=2,
     concurrency=1,
     #  meta_template=internlm_meta_template,
     run_cfg=dict(num_gpus=1, num_procs=1),
)
models = [internlm2_chat_7b]

```

- 评测启动！

```shell
python run.py configs/eval_turbomind.py -w 指定结果保存路径
```

### `KV Cache`量化评测 

- 转换为`TurbMind`

```shell
lmdeploy convert internlm2-chat-7b  模型路径 --dst-path 转换后模型路径
```

- 计算与获得量化参数

```shell
# 计算
lmdeploy lite calibrate 模型路径 --calib-dataset 'ptb' --calib-samples 128 --calib-seqlen 2048 --work-dir 参数保存路径
# 获取量化参数
lmdeploy lite kv_qparams 参数保存路径 转换后模型路径/triton_models/weights/ --num-tp 1
```

- 更改`quant_policy`改成`4`,更改上述`config`里面的路径
- 评测启动！

```shell
python run.py configs/eval_turbomind.py -w 结果保存路径
```

结果文件可在同目录文件[results](./results)中获取

## 致谢

<div align="center">


***感谢上海人工智能实验室组织的 书生·浦语实战营 学习活动~***

***感谢 OpenXLab 对项目部署的算力支持~***

***感谢 浦语小助手 对项目的支持~***
</div>
