import os
import json
from local_preprocessing.photo_to_txt import pdf_to_txt
from Text_summaries_1.main import Text_1_main
from Text_summaries_2.main import combination_main
from Text_summaries_3.main import final_output

if __name__ == "__main__":
    try:
        config_path = os.path.join('config', 'config.json')
        with open(config_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
    except FileNotFoundError:
        print("未找到 config.json 文件，请检查文件是否存在。")    
    except json.JSONDecodeError:
        print("config.json 文件格式错误，请检查文件内容。")
            
    # DRAMA = input("请输入剧本名称：\n")
    # AVATAR = input("请输入人物名称：\n")
    
    DRAMA = "归途七万里"
    AVATAR = "张眷信"
    
    pdf_to_txt(DRAMA)
    
    for _ in range(3):
        Text_1_main(DRAMA)
        
    combination_main(DRAMA)
    
    if AVATAR != None:
        final_output(DRAMA , AVATAR)