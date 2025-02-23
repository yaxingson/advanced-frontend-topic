# 人工智能

## 背景

### 历史背景

- AI的起源：AI的概念最早可以追溯到20世纪50年代，当时科学家们开始探讨是否可以通过机器模仿人类智能，图灵提出了“机器能否思考”的问题，1956年的***达特茅斯会议***被认为是AI作为一个独立领域的开端
- 多次浪潮与低谷：早期的AI研究主要集中在符号处理和规则推理，开发了许多早期的AI程序，如“逻辑理论家”和“学生”等，AI经历了多次发展浪潮（如20世纪80年代的专家系统热潮）和低谷（如“AI寒冬”），但每次低谷后都因技术进步而重新崛起
- 近年来的爆发：2010年后，随着深度学习技术的突破，AI进入快速发展期，应用场景不断扩展

### 技术进步

#### 理论基础

1950年代，艾伦·图灵提出了“图灵测试”，为机器智能的定义提供了理论基础。数学家和逻辑学家们在形式系统、算法和计算理论方面进行了重要研究，为后来的AI打下基础
1980年代，专家系统的兴起使得AI在某些领域（如医疗和金融）得到了应用
随着计算能力的提升和数据存储技术的发展，机器学习特别是深度学习的研究逐渐成为AI研究的热点

从早期的符号主义到连接主义，再到深度学习的兴起，AI理论不断演进。
AI的许多灵感来源于对人类大脑和自然界的模仿，例如神经网络的结构设计。
AI的发展受益于数学、计算机科学、神经科学、心理学等多学科的交叉融合

#### 计算能力

随着计算能力的增强，尤其是图形处理单元（GPU）的发展，使得大规模并行计算成为可能，这为深度学习等复杂模型的训练提供了硬件支持。计算机的普及和性能提升为人工智能提供了强大的计算能力和存储空间。这使得机器能够模拟人类的认知、学习和推理等智能行为。
网络技术、大数据技术和云计算等新兴技术的成熟和普及，进一步推动了人工智能的应用和发展。这些技术为人工智能提供了更广泛的数据来源和更高效的数据处理能力，使得人工智能能够实现更广泛的应用和更高效的学习

#### 大数据

互联网和物联网的普及产生了海量数据，为AI训练提供了丰富的资源。大数据技术的进步也允许更有效的数据处理和分析，数据是AI发展的核心驱动力之一

#### 算法的突破

近年来，深度学习、强化学习等算法的创新（如卷积神经网络CNN、生成对抗网络GAN、循环神经网络（RNNs）及其变种等）极大推动了AI在图像识别、自然语言处理等领域的应用

#### 开源工具和框架

TensorFlow、PyTorch等开源框架的普及降低了AI开发的门槛，促进了全球范围内的技术共享和创新

### 社会背景

- 数字化转型：社会各行业对自动化和智能化的需求日益增长，AI成为推动数字化转型的关键技术
- 降低劳动成本：在许多国家，劳动力成本上升促使企业寻求AI技术来替代或辅助人工，提高效率。
- 消费者需求变化：人们对个性化服务、智能推荐、语音助手等AI驱动的应用需求不断增加

### 政策和伦理

- 国家战略支持：许多国家将AI列为国家战略重点，出台政策支持AI研究和产业化（如中国的《新一代人工智能发展规划》、美国的《国家人工智能研究与发展战略》），例如中国在“新一代人工智能发展规划”中提出，
到2025年基本形成人工智能产业体系，成为全球人工智能创新中心。这些政策为人工智能的发展提供了有力的保障和推动
- 伦理与监管需求：随着AI技术的广泛应用，隐私保护、算法公平性、责任归属等伦理问题引发关注，推动了相关研究和政策制定

## 理论基础

人工智能的三大主义:

1. 符号主义的逻辑推理

2. 连接主义的数据驱动

3. 行为主义的强化学习


### 数学推导

### 机器学习

#### 深度学习

本质是深层的神经网络模型

#### 无监督学习

#### 监督学习

#### 半监督学习

#### 强化学习

### 自然语言处理

发展阶段:

1. 基于规则的手动学习
2. 基于统计的机器学习
3. 基于Embeding的深度学习
4. 预训练和大语言模型

核心任务: 自然语言理解（NLU）和自然语言生成（NLG）


### 计算机视觉

卷积神级网络


#### 物体检测


#### 人脸识别


### 大语言模型

> 大模型: 指拥有数十亿或数百亿个参数的大型预训练语言模型

语言模型：一种用于计算词序列概率的统计模型，旨在评估特定词序列在语言中出现的可能性

语言建模的发展: 

1. 统计语言模型
2. 神经语言模型
3. 预训练语言模型
4. 大模型

> Transformer架构：编码器和解码器

多头自注意力机制

《Attention Is All You Need》


主流的大模型: [GPT-4]()、[BERT]()、[Gemini]()、[Llama]()、[Claude]()和[Deepseek]()

大模型分类:

- 文本大模型
- 视觉大模型
- 语音大模型
- 多模态大模型
- Embedding大模型
- 审查大模型

> 指令模型和推理模型

**AI幻觉**

优化大模型表现的手段：

1. 模型蒸馏
2. 模型微调
3. RAG


常见的AI需求: 决策需求、分析需求、创造性需求、验证性需求和执行需求

私有部署蒸馏版本的Deepseek模型

- <https://ollama.com/>
- <https://dify.ai/>

预训练（Pre-train）:

- 词嵌入：数据压缩后的特征向量
- 向量存储


微调（Fine-tuning）：

- 参数高效微调（Parameter-Efficient Fine-Tuning, PEFT）


> 涌现：上下文学习（ICL）、指令微调和逐步推理（COT）

LLM应用开发范式:

- `Copilot`
- `Plugins`
- `AutoGPT`

LLM业务架构:

- `Embedded模式`
- `Copilot模式`
- `Agents模式`

AI智能体（AI Agent）：指具备自主决策和执行能力的智能系统，能够感知环境、分析信息并采取行动以实现特定目标

> 价值观对齐


### 发展阶段

#### Prompt

#### Agent

#### RAG

### AIGC

> 扩散模型

判别式AI

- 推荐系统
- 人脸识别
- 文字识别
  
生成式AI:

- 文本生成
- 图像生成
- 音频生成
- 视频生成
- 策略生成

内容生产模式的转变: 专家生产内容、用户生产内容、AI辅助生产内容和AI生产内容



### 关键技术

#### WebNN


## 库

- [pytorch](https://github.com/pytorch/pytorch)
- [tensorflow](https://github.com/tensorflow/tensorflow)
- [tensorflow.js](https://github.com/tensorflow/tfjs)
- [brain.js](https://github.com/BrainJS/brain.js/)
- [synaptic](https://github.com/cazala/synaptic)
- [ml5](https://github.com/ml5js/ml5-library)
- [convnetjs](https://github.com/karpathy/convnetjs)
- [xyflow](https://github.com/xyflow/xyflow)
- [langchain](https://github.com/langchain-ai/langchain)
- [@xenova/transformers]()
- [@pinecone-database/pinecone](https://github.com/pinecone-io/pinecone-ts-client)
- [ollama](https://github.com/ollama/ollama)
- [dify](https://github.com/langgenius/dify)
- [scikit-learn](https://github.com/scikit-learn/scikit-learn)
- [sora](https://github.com/hpcaitech/Open-Sora)
- [StableVideo](https://github.com/rese1f/StableVideo)
- [matplotlib](https://github.com/matplotlib/matplotlib)
- [numpy](https://github.com/numpy/numpy)
- [pandas](https://github.com/pandas-dev/pandas)


## 样例

## 应用场景

### AI应用开发平台

研发步骤:

1. 选取模型
2. 工作流程编排
3. 应用服务化

开源平台:

- <https://github.com/langgenius/dify>
- <https://github.com/Mintplex-Labs/anything-llm>



### Prompt工程应用

> Prompt: 一个输入的文本段落或短语，作为生成模型输出的起点或引导

Prompt提示语技巧:

- 角色扮演
- 零样本（Zero-shot）、单样本（One-shot）和少量样本（Few-shot）
- 思维链（COT）和思维树（TOT）
- 外部工具
- 输出提示
- 自洽性 


提示语框架: TASTE、ALIGN、RTGO和COSTAR

提示语的构造要素：

- 指令：核心任务
- 上下文：任务描述/背景
- 期望（包括输入数据和输出提示）

```txt
> let's think step by step.

```

> 提示语链

<https://api-docs.deepseek.com/zh-cn/prompt-library/>

<https://kimi.moonshot.cn/>

> 乔哈里视窗

Prompt安全防范


### 超级个体

### 数字虚拟人

### 智能客服与机器人

### 内容创作

## 资源

- <https://hugging-face.cn/>
- <https://www.langchain.com/langsmith>
- <https://metaso.cn/>
- <https://siliconflow.cn/>
- <https://devv.ai/>
- <https://discord.com/>
- <https://app.runwayml.com>
- <https://pika.art/>
- <https://vivago.ai>
- <https://klingai.kuaishou.com/>
- <https://noisee.com.cn/#/>
- <https://jimeng.jianying.com/>


