import openai
from typing import Dict, Optional
import logging
from datetime import datetime

class ContentGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model_name = "gpt-3.5-turbo"
        openai.api_key = api_key
        self.logger = logging.getLogger("ContentGenerator")

    def generate_blog_post(self, topic: str) -> Dict:
        """Generates a high-quality blog post based on the given topic."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", 
                     "content": f"You are a professional blogger. Write a detailed article about {topic}."},
                    {"role": "user", "content": f"Write a blog post on {topic}"}
                ],
                max_tokens=2000
            )
            
            if not response.choices:
                self.logger.error("No choices in OpenAI response")
                return {"error": "Failed to generate content"}
            
            content = response.choices[0].message.content.strip()
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "topic": topic,
                "status": "generated"
            }
            
            self.logger.info(f"Generated blog post on {topic}")
            return {"content": content, "metadata": metadata}
            
        except Exception as e:
            self.logger.error(f"Error generating content: {str(e)}", exc_info=True)
            raise

    def validate_content(self, content: str) -> bool:
        """Validates the generated content for quality."""
        try:
            # Simulate basic validation
            if len(content) < 500:
                self.logger.warning("Generated content too short")
                return False
            
            if not any(word in content.lower() for word in ["introduction", "conclusion", "step-by-step"]):
                self.logger.warning("Content missing required sections")
                return False
                
            self.logger.info("Content validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}", exc_info=True)
            raise