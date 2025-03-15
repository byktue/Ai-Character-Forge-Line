# Ai-Character-Forge-Line 1.0.3.

**AI-Powered Character Persona Extraction & Simulation Toolkit**

  

多次、多线程调用现有的ai模型，比如deepseek，根据已有文本，批量化、精细化、精准化生成人设

Repeatedly and multi-threadedly call the existing AI model (DeepSeek) to generate character personas in a batch, refined, and precise manner based on the provided text.


[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)

## 🚀 项目概述

**Ai-Character-Forge-Line** 是一个用于处理文本信息，提取文本中主要人物相关信息（如角色身份、性格特点、话语信息等）的项目。该项目通过调用 DeepSeek API 来完成信息提取，并将处理结果保存到指定的输出文件夹中。

## ✨ 项目作者

#### 项目主要作者：byktue

- 所在学校：华东师范大学
- 所在院系与专业：数据科学与工程学院  数据科学与大数据

**联系方式：**
- 邮箱： yangbyktue@gmail.com
	10235501403@stu.ecnu.edu.cn
	228900195@qq.com
- 微信：wx228900195
- QQ：228900195

##### 项目合作者：duringbug


## 🚀 使用流程
因为项目当前还未开发、优化完全，所以并未形成自动化工作流

1. 将项目的src文件夹从github下载到本地
2. 在src/config/config.json中输入相应的配置
3. 将需要处理的长文本文件存储到前面配置文件中的地址，如果是pdf格式的文件，则运行src/local preprocessing/photo_to_txt.py
4. 进行初步文本处理，运行src/Text summaries_1/run_parallel.py
5. 进行二次文本处理，运行src/Text summaries_2/main combination.py
6. 进行三次文本处理，得到相应人设，运行src/Text summaries_3/main.py

## ✨ 项目实现功能

- **pdf转txt**：网络上剧本杀的文本素材大多以pdf存储，在本地预处理将pdf转为txt，有利于后续操作减少成本

- **批量多线程处理**：Text summaries_1 文件夹中，在对长文本进行多线程降维处理时，已实现程序并行

- **精准细节提取**：结合规则引擎与DeepSeek模型，把文本内容总结为角色性格、事件、外貌等多个方面，多线程拉取Deepseek的api进行文本总结处理，确保精细化

- **生成markdown格式的人设**：将多线程处理好的维度进行汇总，按特定格式生成符合的markdown格式的人设


## 🚀 项目结构

data 文件夹用于存储数据，src文件夹用于存储代码和配置

**配置文件**
- src/config/config.json：包含项目的输入输出文件夹路径、编码方式以及 DeepSeek API 的 URL 等配置信息。

**pdf转txt**
- src/local preprocessing/photo_to_txt.py：提取pdf文件中的文本信息，并按原本的文件结构进行存储（保持原本的文件夹嵌套顺序）

**初次文本处理**
- 位于src/Text summaries_1
- 划分多个板块拉取deepseek的api进行相应的处理，比如name文件夹中，就是处理相应的名字和别名信息。
- src/Text summaries_1/run_parallel.py 文件，则是将多线程并行运行的程序，在初次文本处理时，运行这个程序即可
- 线程中处理的结果，依旧是按照原本的文件结构进行存储

**二次文本处理**
- 位于src/Text summaries_2
- 将初次文本处理后的同一类的文件，汇总到一个文本文件中，比如对于events维度进行处理之后，将events初次处理后的文件夹中的所有文件，全部汇聚到一个txt文件中
- 删除空文件和无效信息，比如有些文件因为没有提取到有效的信息，仍会保留着 ”对于文本中角色的话语信息：角色话语：请提供文本内容，我将帮助提取角色的话语。” 之类的无效信息
- 核心代码为src/Text summaries_2/main combination.py

**三次文本处理**
- 位于src/Text summaries_3
-  根据用户输入的人物名称，拉取deepseek的api，对二次文本处理后的不同维度进行处理，进行汇总，形成具有丰富细节的人物人设
- 主代码为src/Text summaries_3/main.py

文件结构为
```
|   README.md
|
+---data
\---src
    |   src.md
    |   __init__.py
    |
    +---config
    |       config.json
    |
    +---local preprocessing
    |   |   photo_to_txt.py
    |   |
    |   \---__pycache__
    |           photo_to_txt.cpython-313.pyc
    |
    +---Text summaries_1
    |   |   run_parallel.py
    |   |
    |   +---appearance
    |   |   |   api_request.py
    |   |   |   config_loader.py
    |   |   |   file_processor.py
    |   |   |   main.py
    |   |   |
    |   |   \---__pycache__
    |   |           api_request.cpython-313.pyc
    |   |           config_loader.cpython-313.pyc
    |   |           file_processor.cpython-313.pyc
    |   |
    |   +---events
    |   |   |   api_request.py
    |   |   |   config_loader.py
    |   |   |   file_processor.py
    |   |   |   main.py
    |   |   |
    |   |   \---__pycache__
    |   |           api_request.cpython-313.pyc
    |   |           config_loader.cpython-313.pyc
    |   |           file_processor.cpython-313.pyc
    |   |
    |   +---identity
    |   |   |   api_request.py
    |   |   |   config_loader.py
    |   |   |   file_processor.py
    |   |   |   main.py
    |   |   |
    |   |   \---__pycache__
    |   |           api_request.cpython-313.pyc
    |   |           config_loader.cpython-313.pyc
    |   |           file_processor.cpython-313.pyc
    |   |
    |   +---name
    |   |   |   api_request.py
    |   |   |   config_loader.py
    |   |   |   file_processor.py
    |   |   |   main.py
    |   |   |
    |   |   \---__pycache__
    |   |           api_request.cpython-313.pyc
    |   |           config_loader.cpython-313.pyc
    |   |           file_processor.cpython-313.pyc
    |   |
    |   +---personality
    |   |   |   api_request.py
    |   |   |   config_loader.py
    |   |   |   file_processor.py
    |   |   |   main.py
    |   |   |
    |   |   \---__pycache__
    |   |           api_request.cpython-313.pyc
    |   |           config_loader.cpython-313.pyc
    |   |           file_processor.cpython-313.pyc
    |   |
    |   +---utterance
    |   |   |   api_request.py
    |   |   |   config_loader.py
    |   |   |   file_processor.py
    |   |   |   main.py
    |   |   |
    |   |   \---__pycache__
    |   |           api_request.cpython-313.pyc
    |   |           config_loader.cpython-313.pyc
    |   |           file_processor.cpython-313.pyc
    |   |
    |   \---__pycache__
    |           api_request.cpython-313.pyc
    |           config_loader.cpython-313.pyc
    |           file_processor.cpython-313.pyc
    |
    +---Text summaries_2
    |   |   combination.py
    |   |   config_loader.py
    |   |   main combination.py
    |   |
    |   \---__pycache__
    |           api_sum.cpython-313.pyc
    |           combination.cpython-313.pyc
    |           config_loader.cpython-313.pyc
    |
    \---Text summaries_3
        |   appearance.py
        |   config_loader.py
        |   events.py
        |   file_checker.py
        |   identity.py
        |   main.py
        |   name.py
        |   personality.py
        |   utterance.py
        |
        \---__pycache__
                appearance.cpython-313.pyc
                config_loader.cpython-313.pyc
                events.cpython-313.pyc
                file_checker.cpython-313.pyc
                identity.cpython-313.pyc
                name.cpython-313.pyc
                personality.cpython-313.pyc
                utterance.cpython-313.pyc
```