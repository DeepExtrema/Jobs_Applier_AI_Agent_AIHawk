
from typing import Dict, Any, List
from src.logger_utils import logger
from src.utils.chrome_utils import init_browser
from src.libs.llm_manager import GeminiModel, GPTAnswerer, AIAdapter
from src.resume_schemas.resume import Resume
from src.job import Job as JobModel
import config as cfg
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

class ApplierAgent:
    """
    Generic Job Applier Agent using Gemini to analyze and fill forms.
    """
    
    # ...

    def __init__(self, llm_api_key: str, data_folder: Path):
        self.driver = init_browser()
        self.llm_api_key = llm_api_key
        self.data_folder = data_folder
        
        # Use Adapter to respect config
        adapter = AIAdapter(cfg, llm_api_key)
        self.llm = adapter.model # This gives us the underlying langchain model
        
        # Load Resume
        resume_path = data_folder / "plain_text_resume.yaml"
        with open(resume_path, "r", encoding="utf-8") as f:
            self.resume_content = f.read()
        self.resume = Resume(self.resume_content)
        
        # Init Answerer
        # Mock config for AIAdapter if needed or pass parsed config
        # Attempting to use existing GPTAnswerer structure
        self.gpt_answerer = GPTAnswerer(cfg, llm_api_key)
        self.gpt_answerer.set_resume(self.resume)
        
    def apply(self, job: Dict[str, str]):
        """
        Main method to apply to a job URL.
        """
        url = job.get('url')
        company = job.get('company')
        role = job.get('role')
        
        logger.info(f"Starting application for {role} at {company}")
        
        # Set Job Context
        job_obj = JobModel(role=role, company=company, link=url, description="Generic Application")
        self.gpt_answerer.set_job(job_obj)
        
        try:
            self.driver.get(url)
            time.sleep(5) # Wait for load
            
            # Analyze form
            form_json = self._analyze_form()
            logger.info(f"Identified fields raw: {form_json}")
            
            try:
                # remove markdown code blocks if present
                clean_json = form_json.replace("```json", "").replace("```", "").strip()
                fields = json.loads(clean_json)
            except json.JSONDecodeError:
                logger.error("Failed to parse form JSON from LLM")
                return

            for field in fields:
                self._fill_field(field)
            
            # Submit logic (Optional, maybe just notify user to review)
            logger.info(f"Form filled for {url}. Please review and submit.")
            
        except Exception as e:
            logger.error(f"Failed to apply to {url}: {e}")

    def _fill_field(self, field: Dict):
        """
        Generates answer and fills a single field.
        """
        field_id = field.get('id')
        field_type = field.get('type')
        label = field.get('label')
        
        if not field_id:
            return
            
        logger.info(f"Processing field: {label} ({field_type})")
        
        # Determine answer
        # For simple fields, use GPTAnswerer
        # For now, let's use a generic prompt if GPTAnswerer doesn't match perfectly
        
        try:
            element = self.driver.find_element(By.XPATH, f"//*[@id='{field_id}'] | //*[@name='{field_id}']")
            
            if field_type in ['text', 'email', 'tel', 'url', 'number']:
                item_to_answer = f"{label} (Type: {field_type})"
                # Reuse the textual question answerer
                answer = self.gpt_answerer.answer_question_textual_wide_range(item_to_answer)
                
                # Cleaning up answer (remove quotes etc)
                answer = str(answer).strip('"')
                
                element.clear()
                element.send_keys(answer)
                logger.info(f"Filled {label} with: {answer}")
                
            elif field_type == 'file':
                # Resume upload
                # Assumption: field label contains "resume" or "cv"
                if "resume" in label.lower() or "cv" in label.lower():
                    # We need a PDF path. user provided yaml.
                    # We might need to generate a PDF first or just upload the text file?
                    # The prompt asked for absolute path of cover letters.
                    # For now skip or use a placeholder path if we had one.
                    pass
            
        except Exception as e:
            logger.warning(f"Failed to fill field {label}: {e}")

            
    def _analyze_form(self) -> str:
        """
        Analyzes the page DOM to identify form fields.
        """
        # Get simplified DOM
        body = self.driver.find_element(By.TAG_NAME, "body")
        inner_html = body.get_attribute("innerHTML")
        
        # Simple cleanup (naive)
        # In a real scenario, we'd use BeautifulSoup to strip scripts/styles
        # For now, let's just assume the LLM can handle it or truncate
        
        # Prompt LLM to identify fields
        prompt = f"""
        Analyze the following HTML form and identify the input fields, textareas, and file uploads.
        Return a JSON list of objects with:
        - "id": The html id or name or xpath selector
        - "type": input type (text, email, file, radio, checkbox, etc)
        - "label": The visible label text
        - "required": boolean
        
        HTML Context (Truncated):
        {inner_html[:10000]} 
        """
        # Note: 10k chars is a limit, might need better chunking
        
        response = self.llm.invoke(prompt)
        return response.content
        
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    from src.logger_utils import logger
    from main import ConfigValidator, FileManager
    from pathlib import Path
    
    try:
        data_folder = Path("data_folder")
        secrets_file = data_folder / "secrets.yaml"
        llm_api_key = ConfigValidator.validate_secrets(secrets_file)
        
        agent = ApplierAgent(llm_api_key, data_folder)
        print("ApplierAgent instantiated successfully.")
        
        # Test Job
        test_job = {
            "company": "Roblox",
            "role": "2026 Data Scientist",
            "url": "https://careers.roblox.com/jobs/7463634?gh_jid=7463634"
        }
        agent.apply(test_job)
        
        input("Press Enter to close browser...")
        agent.close()
    except Exception as e:
        logger.error(f"Test failed: {e}")
