# LOL智能小助手

***Chat-LoL 模型下载地址：[https://www.modelscope.cn/models/kmno4zx/huanhuan-chat-internlm2/summary](https://www.modelscope.cn/models/wjh2001/Chat_LoL/summary)***
> *此仓库主要用于将 LOL智能小助手项目部署到 ModelScope 。*

## 介绍

&emsp;&emsp;LOL智能小助手基于[InternLM-chat-7b](https://github.com/InternLM/InternLM.git)基座模型，是利用op.gg官网上的部分数据进行LoRA方法微调，以及B站中的视频攻略(转文本)作为RAG向量知识库文本，完成的LOL智能小助手问答demo。





## 数据集

&emsp;&emsp;lol智能小助手 数据集采用OPGG的胜率、出场率、弱势英雄、当前版本的level等组成200余条，将每条数据完成扩充后，共计【11400】余条，用扩充后的数据集完成LORA微调，数据集样例：


![数据集样例.png](https://github.com/2001wjh/InternLM_LoL_assistant/blob/main/image/%E6%95%B0%E6%8D%AE%E9%9B%86%E6%A0%B7%E4%BE%8B.png)


​		可以使用仓库中utils文件夹中的脚本【spider_opgg.py】完成opgg的爬取，并使用脚本【generate_data.py】完成数据集的扩充。

## RAG

​		RAG就是通过检索获取相关的知识并将其融入Prompt，让大模型能够参考相应的知识从而给出合理回答。因此，可以将RAG的核心理解为“检索+生成”，前者主要是利用向量数据库的高效存储和检索能力，召回目标知识；后者则是利用大模型和Prompt工程，将召回的知识合理利用，生成目标答案。

完整的RAG应用流程主要包含两个阶段：

- 数据准备阶段：数据提取——>文本分割——>向量化（embedding）——>数据入库

- 应用阶段：用户提问——>数据检索（召回）——>注入Prompt——>LLM生成答案

​		LOL智能小助手使用的是从B站攻略视频中生成的攻略文字，字数逾10w+，完成知识库构建。使用到开源词向量模型 Sentence Transformer完成embedding，借助开源第三方库NLTK完成tokenize和tagger。使用 LangChain 提供的 FileLoader 对象来加载目标文件，得到由目标文件解析出的纯文本内容。

## 微调

&emsp;&emsp;有两种方案，我更倾向于使用 XTuner 训练， XTuner 有各个模型的一键训练脚本，很方便。且对 InternLM2 的支持度最高。

### 方案一：Transformers 

&emsp;&emsp;使用 Transformers 的 Trainer 进行微调。

### 方案二：XTuner

&emsp;&emsp;使用 XTuner 进行微调，具体脚本可参考[internlm_chat_7b_qlora_opgg2024_e3.py](https://github.com/2001wjh/InternLM_LoL_assistant/blob/main/train/internlm_chat_7b_qlora_opgg2024_e3.py))，该脚本在`train`文件夹下。脚本内有较为详细的注释。

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





## 致谢

<div align="center">


***感谢上海人工智能实验室组织的 书生·浦语实战营 学习活动~***

***感谢 OpenXLab 对项目部署的算力支持~***

***感谢 浦语小助手 对项目的支持~***
</div>
