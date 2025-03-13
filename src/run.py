from local_preprocessing.photo_to_txt import pdf_to_txt
from Text_summaries_1.main import Text_1_main
from Text_summaries_2.main import combination_main
from Text_summaries_3.main import final_output

    
def run_main():
    pdf_to_txt()
    Text_1_main()
    combination_main()
    final_output()
    return None

if __name__ == "__main__":
    run_main()