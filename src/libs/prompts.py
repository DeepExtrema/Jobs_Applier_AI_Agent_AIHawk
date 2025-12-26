
# Prompts for the AI Agent
from src.utils.constants import (
    AVAILABILITY,
    CERTIFICATIONS,
    COVER_LETTER,
    EDUCATION_DETAILS,
    EXPERIENCE_DETAILS,
    INTERESTS,
    LANGUAGES,
    LEGAL_AUTHORIZATION,
    PERSONAL_INFORMATION,
    PROJECTS,
    SALARY_EXPECTATIONS,
    SELF_IDENTIFICATION,
    WORK_PREFERENCES,
)

summarize_prompt_template = """
You are an expert HR assistant. Your task is to summarize the following job description. Keys details to extract:
- Role Title
- Key Skills Required
- Years of Experience
- Core Responsibilities
- Company Culture/Values

Job Description:
{text}

Summary:
"""

personal_information_template = """
Answer the job application question based on the candidate's Personal Information.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

self_identification_template = """
Answer the job application question based on the candidate's Self Identification details.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

legal_authorization_template = """
Answer the job application question based on the candidate's Legal Authorization details.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

work_preferences_template = """
Answer the job application question based on the candidate's Work Preferences.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

education_details_template = """
Answer the job application question based on the candidate's Education Details.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

experience_details_template = """
Answer the job application question based on the candidate's Experience Details.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

projects_template = """
Answer the job application question based on the candidate's Projects.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

availability_template = """
Answer the job application question based on the candidate's Availability.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

salary_expectations_template = """
Answer the job application question based on the candidate's Salary Expectations.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

certifications_template = """
Answer the job application question based on the candidate's Certifications.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

languages_template = """
Answer the job application question based on the candidate's Languages.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

interests_template = """
Answer the job application question based on the candidate's Interests.
Question: {question}
Candidate Profile: {resume_section}

Answer:
"""

coverletter_template = """
Write a professional cover letter for the following job.
Candidate Resume: {resume}
Job Description: {job_description}
Company: {company}

Cover Letter:
"""

determine_section_template = f"""
Identify which section of the resume is most relevant to answer the following question.
Options: [Personal information, Self Identification, Legal Authorization, Work Preferences, Education Details, Experience Details, Projects, Availability, Salary Expectations, Certifications, Languages, Interests, Cover letter]

Question: {{question}}

Section:
"""

numeric_question_template = """
Extract or calculate a numeric answer for the following question based on the resume.
Question: {question}
Education: {resume_educations}
Experience: {resume_jobs}
Projects: {resume_projects}

Provide ONLY the number.
Answer:
"""

options_template = """
Select the best option from the provided list to answer the question based on the candidate profile.
Question: {question}
Options: {options}
Candidate Profile:
{resume}
{job_application_profile}

Best Option:
"""

resume_or_cover_letter_template = """
Determine if the following phrase is asking for a Resume or a Cover Letter.
Phrase: {phrase}

Answer (resume/cover):
"""

is_relavant_position_template = """
Assess if the candidate's profile is suitable for the job description.
Candidate: {resume}
Job: {job_description}

Provide a Score (0-10) and Reasoning.
Format:
Score: [score]
Reasoning: [text]
"""
