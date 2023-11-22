'''
-----------------------------------------------------------------------
File: auto_apply_model.py
Creation Time: Nov 21st 2023 2:49 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import json
from utils.llm_models import ChatGPT
from utils.data_extraction import get_url_content

class AutoApplyModel:
    def __init__(self, openai_key: str):
        self.openai_key = openai_key
    
    def get_system_prompt(self, system_prompt_path: str):
        """
        Reads the system prompt text from the specified file path.

        Args:
            system_prompt_path (str): The file path of the system prompt.

        Returns:
            str: The system prompt read from the file.
        """
        return open(system_prompt_path).read().strip()+"\n"

    def extract_job_details(self, url: str):
        """
        Extracts job details from the specified job URL.

        Args:
            url (str): The URL of the job posting.

        Returns:
            dict: A dictionary containing the extracted job details.
        """   

        system_prompt = self.get_system_prompt("job_llm/prompts/persona-job-llm.txt") + \
                        self.get_system_prompt("job_llm/prompts/extract-job-detail.txt")
        job_site_content = get_url_content(url)

        chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
        response = chat_gpt.get_response(job_site_content)
        job_details = json.loads(response)
        
        return job_details
    
    def generate_resume_details(self, job_details: dict, user_data: dict):
        system_prompt = self.get_system_prompt("job_llm/prompts/persona-job-llm.txt") + \
                        self.get_system_prompt("job_llm/prompts/generate-resume-details.txt")
        query = f"""Provided Job description delimited by triple backticks(```) and \
                    my resume or work information below delimited by triple dashes(---).
                    ```
                    {json.dumps(job_details)}
                    ```

                    ---
                    {json.dumps(user_data)}
                    ---
                """
        
        chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
        response = chat_gpt.get_response(query)
        job_details = json.loads(response)
        return job_details
    
    def generate_cover_letter(self, job_details: dict, user_data: dict):
        system_prompt = self.get_system_prompt("job_llm/prompts/persona-job-llm.txt") + \
                        self.get_system_prompt("job_llm/prompts/generate-cover-letter.txt")
        query = f"""Provided Job description delimited by triple backticks(```) and \
                    my resume or work information below delimited by triple dashes(---).
                    ```
                    {json.dumps(job_details)}
                    ```

                    ---
                    {json.dumps(user_data)}
                    ---
                """
        
        chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
        cover_letter = chat_gpt.get_response(query)
        return cover_letter
