'''
-----------------------------------------------------------------------
File: demo.py
Creation Time: Nov 1st 2023 3:08 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''
import re
import json
from job_llm import config
from job_llm.utils.llm_models import ChatGPT
from job_llm.utils.data_extraction import get_link_content
from datetime import datetime

def main(url: str):
    system_prompt = open("./job_llm/prompts/job-detail-extractor.txt").read().strip()
    web_content_prompt = get_link_content(url)

    chat_gpt = ChatGPT(openai_api_key=config.OPENAI_API_KEY, system_prompt=system_prompt)
    response = chat_gpt.get_response(web_content_prompt)

    response['link'] = url
    
    # file_path = f"output/demo-result_{int(datetime.timestamp(datetime.now()))}.json"
    file_name = f"JD-{re.sub(r'[^a-zA-Z]', '', response['title'])}.json"
    file_path = f"output/{file_name}"

    with open(file_path, 'w') as file:
        json.dump(response,file)
    
    print(response)

if __name__ == "__main__":
    main("https://simplify.jobs/p/7769bcc5-81cc-44e7-955b-c5d183554f00/Intern--Full-Stack-Engineer")