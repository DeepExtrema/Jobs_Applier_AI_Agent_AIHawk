
import requests
import re
from typing import List, Dict

class JobCollector:
    """
    Collects job URLs from the speedyapply/2026-AI-College-Jobs repository.
    """
    
    BASE_URL = "https://raw.githubusercontent.com/speedyapply/2026-AI-College-Jobs/main/"
    FILES_TO_CHECK = [
        "NEW_GRAD_USA.md",
        # "INTERN_USA.md" # Assuming this exists or similar, based on repo structure clues
    ]

    def __init__(self):
        self.jobs = []

    def fetch_job_links(self) -> List[Dict[str, str]]:
        """
        Fetches markdown content from the repository and extracts job links.
        Returns a list of dictionaries with 'company' and 'url'.
        """
        all_jobs = []
        
        # We manually add NEW_GRAD_USA.md as confirmed. 
        # Ideally we would list all files but let's start with the one we know exists and has content.
        target_files = ["NEW_GRAD_USA.md"] 

        for filename in target_files:
            url = f"{self.BASE_URL}{filename}"
            try:
                print(f"Fetching jobs from {url}...")
                response = requests.get(url)
                response.raise_for_status()
                content = response.text
                print(f"Content length: {len(content)}")
                print(f"First 500 chars: {content[:500]}")
                jobs = self._parse_markdown_links(content)
                print(f"Found {len(jobs)} jobs in {filename}")
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"Error fetching {filename}: {e}")
        
        self.jobs = all_jobs
        return all_jobs

    def _parse_markdown_links(self, markdown_content: str) -> List[Dict[str, str]]:
        """
        Parses HTML table rows from the content to extract job details.
        Expected format: | Company | Role | Location | Salary | Apply Link | Date |
        """
        jobs = []
        lines = markdown_content.split('\n')
        
        # Regex for company name: <a ...><strong>Name</strong></a>
        company_pattern = re.compile(r'<strong>(.*?)</strong>')
        # Regex for apply link: <a href="(...)"
        apply_link_pattern = re.compile(r'<a href="([^"]+)"')
        
        for line in lines:
            if "|" not in line or "---" in line:
                continue
                
            parts = line.split("|")
            if len(parts) < 6:
                continue
            
            # parts[0] is empty if line starts with |
            # parts[1] is Company
            # parts[2] is Role
            # parts[5] is Apply Link column
            
            try:
                company_col = parts[1]
                role_col = parts[2]
                apply_col = parts[5]
                
                # Extract Company
                company_match = company_pattern.search(company_col)
                if not company_match:
                    continue
                company = company_match.group(1)
                
                # Extract Role
                role = role_col.strip()
                
                # Extract URL
                url_match = apply_link_pattern.search(apply_col)
                if not url_match:
                    continue
                url = url_match.group(1)
                
                # Filter out generic or empty
                if url and "http" in url:
                    jobs.append({
                        "company": company,
                        "role": role,
                        "url": url
                    })
                    # print(f"Found Job: {company} - {role} -> {url[:50]}...")
            except Exception as e:
                # print(f"Error parsing line: {line[:50]}... {e}")
                pass
        
        return jobs

if __name__ == "__main__":
    collector = JobCollector()
    jobs = collector.fetch_job_links()
    print(f"Total jobs found: {len(jobs)}")
    if jobs:
        print(f"First 5 jobs: {jobs[:5]}")
