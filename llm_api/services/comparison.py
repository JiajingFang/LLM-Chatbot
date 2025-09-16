from fastapi import HTTPException
from pydantic import BaseModel
from llm_api.utils.logger import get_logger
from llm_api.config import settings
import openai
from typing import Optional, Dict, Any

logger = get_logger(__name__)

openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


async def compare_with_openai(claude_resp: str, openai_resp: str) -> Dict[str, str]:
    """Use OpenAI to compare and summarize responses"""
    try:
        # Summary prompt
        summary_prompt = f"""
        Please provide a concise summary of the key points from these two AI responses to the same question:

        Response 1 (Claude):
        {claude_resp}

        Response 2 (OpenAI):
        {openai_resp}

        Summary:
        """

        # Comparison prompt
        comparison_prompt = f"""
        Compare these two AI responses in detail:

        Claude Response:
        {claude_resp}

        OpenAI Response:
        {openai_resp}

        Please analyze:
        1. Key similarities and differences
        2. Quality and accuracy of information
        3. Writing style and approach
        4. Completeness of the answers
        5. Which aspects each response handles better

        Comparison:
        """

        # Run both requests concurrently
        summary_task = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=500
        )
        
        comparison_task = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": comparison_prompt}],
            max_tokens=800
        )

        summary = summary_task.choices[0].message.content
        comparison = comparison_task.choices[0].message.content

        return {
            "summary": summary,
            "comparison": comparison
        }
    except Exception as e:
        logger.error(f"OpenAI comparison error: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {e}")
