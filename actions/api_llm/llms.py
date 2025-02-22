import json
import logging
import os
from typing import Optional, Text, Dict

import openai
from dotenv import load_dotenv
    
load_dotenv()
logger = logging.getLogger(__name__)


class OpenAI:
    def __init__(
        self,
        completions_model=os.environ.get(
            "OPENAI_COMPLETIONS_MODEL", "text-davinci-003"
        ),
        completions_temperature=int(
            os.environ.get("OPENAI_COMPLETIONS_TEMPERATURE", 0)
        ),
        completions_max_tokens=int(
            os.environ.get("OPENAI_COMPLETIONS_MAX_TOKENS", 100)
        ),
        completions_api_key=os.environ.get("OPENAI_COMPLETIONS_API_KEY", None),
    ):
        self.completions_model = completions_model
        self.completions_temperature = completions_temperature
        self.completions_max_tokens = completions_max_tokens
        self.completions_api_key = completions_api_key

    @staticmethod
    def _extract_text_response(choices: Dict) -> Optional[Text]:
        try:
            choice = choices[0].get("text", "")
            logger.info(f"LLM response: \n{choice}\n")

            response_json = json.loads(choice)
            return response_json.get("answer", None)
        except Exception as e:
            logger.exception(f"Error occurred while extracting the LLM response. {e}")
            return None

    def get_text_completion(self, prompt: Text) -> Optional[Text]:
        logger.info(f"LLM prompt: \n{prompt}\n")

        openai.api_key = self.completions_api_key

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        try:
            response = openai.chat.completions.create(
                model=self.completions_model,
                messages=messages,
                temperature=self.completions_temperature,
                max_tokens=self.completions_max_tokens,
            )
            return response['choices'][0]['text'].strip() if response['choices'] else ""
        except Exception as e:
            # Handle exceptions as needed
            print(f"Error: {e}")
            return ""

