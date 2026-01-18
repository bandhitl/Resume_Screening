import os
from typing import Dict, Any, Optional
from anthropic import Anthropic
from openai import OpenAI


class AIAnalyzer:
    """Use AI (Claude or GPT) to analyze and score resumes."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "anthropic"):
        """Initialize the AI analyzer with API key and provider.

        Args:
            api_key: The API key for the selected provider
            provider: Either "anthropic" or "openai"
        """
        self.provider = provider.lower()

        if self.provider == "anthropic":
            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            if not self.api_key:
                raise ValueError(
                    "Anthropic API key not found. Please provide ANTHROPIC_API_KEY."
                )
            self.client = Anthropic(api_key=self.api_key)
        elif self.provider == "openai":
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key not found. Please provide OPENAI_API_KEY."
                )
            self.client = OpenAI(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'anthropic' or 'openai'")

    def analyze_resume(
        self,
        resume_text: str,
        criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze a resume against screening criteria using AI.

        Args:
            resume_text: The text content of the resume
            criteria: Dictionary containing screening criteria including job description

        Returns:
            Dictionary with analysis results including score and details
        """
        prompt = self._build_analysis_prompt(resume_text, criteria)

        try:
            if self.provider == "anthropic":
                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2500,
                    temperature=0,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                response_text = message.content[0].text

            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }],
                    max_tokens=2500,
                    temperature=0
                )
                response_text = response.choices[0].message.content

            return self._parse_analysis_response(response_text)

        except Exception as e:
            print(f"Error analyzing resume with AI: {e}")
            return {
                "error": str(e),
                "overall_score": 0,
                "analysis": "Failed to analyze resume"
            }

    def _build_analysis_prompt(self, resume_text: str, criteria: Dict[str, Any]) -> str:
        """Build the prompt for AI analysis."""
        job_description = criteria.get('job_description', '')

        if job_description:
            # Use job description-based analysis
            prompt = f"""You are an expert HR recruiter analyzing resumes. Compare the following resume against the job description to determine if the candidate should be invited for an interview.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text[:4000]}

Please provide a detailed analysis in the following format:

OVERALL SCORE: [0-100]
[Rate how well the candidate matches the job description]

INTERVIEW RECOMMENDATION: [Yes / No / Maybe]
[Should this candidate be invited for an interview?]

KEY QUALIFICATIONS MATCH: [0-100]
[How well do their qualifications match the job requirements?]

SKILLS ASSESSMENT: [0-100]
[Do they have the required skills? Rate and explain]

EXPERIENCE ASSESSMENT: [0-100]
[Does their experience align with what the job requires?]

EDUCATION ASSESSMENT: [0-100]
[Does their education meet the requirements?]

STRENGTHS:
[List 3-5 key strengths that make them a good fit for THIS job]

GAPS & CONCERNS:
[List 2-3 areas where they don't meet the job requirements]

INTERVIEW QUESTIONS:
[Suggest 3-4 specific interview questions based on gaps or strengths]

SUMMARY:
[2-3 sentences explaining why they should or should not be interviewed]
"""
        else:
            # Use criteria-based analysis (fallback)
            prompt = f"""You are an expert HR recruiter analyzing resumes. Please analyze the following resume against the given criteria.

Resume:
{resume_text[:4000]}

Screening Criteria:
- Job Title: {criteria.get('job_title', 'Not specified')}
- Required Skills: {criteria.get('skills', 'Not specified')}
- Experience Level: {criteria.get('experience', 'Not specified')}
- Education: {criteria.get('education', 'Not specified')}
- Additional Requirements: {criteria.get('additional_notes', 'None')}

Please provide a detailed analysis in the following format:

OVERALL SCORE: [0-100]

INTERVIEW RECOMMENDATION: [Yes / No / Maybe]
[Should this candidate be invited for an interview?]

SKILLS MATCH: [0-100]
[Explain which skills match and which are missing]

EXPERIENCE ASSESSMENT: [0-100]
[Evaluate if the experience level matches requirements]

EDUCATION ASSESSMENT: [0-100]
[Evaluate if education meets requirements]

STRENGTHS:
[List 3-5 key strengths]

GAPS & CONCERNS:
[List 2-3 areas where the candidate falls short]

INTERVIEW QUESTIONS:
[Suggest 3-4 specific interview questions]

SUMMARY:
[2-3 sentence summary of the candidate's fit]
"""

        return prompt

    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response into structured data."""
        result = {
            "overall_score": 0,
            "skills_score": 0,
            "experience_score": 0,
            "education_score": 0,
            "qualifications_score": 0,
            "strengths": [],
            "weaknesses": [],
            "interview_questions": [],
            "interview_recommendation": "",
            "recommendation": "",
            "summary": "",
            "detailed_analysis": response_text
        }

        lines = response_text.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()

            if line.startswith('OVERALL SCORE:'):
                try:
                    result['overall_score'] = int(line.split(':')[1].strip().split()[0])
                except (ValueError, IndexError):
                    pass

            elif line.startswith('INTERVIEW RECOMMENDATION:'):
                result['interview_recommendation'] = line.split(':', 1)[1].strip()
                result['recommendation'] = result['interview_recommendation']
                current_section = None

            elif line.startswith('KEY QUALIFICATIONS MATCH:'):
                try:
                    result['qualifications_score'] = int(line.split(':')[1].strip().split()[0])
                except (ValueError, IndexError):
                    pass
                current_section = 'qualifications'

            elif line.startswith('SKILLS MATCH:') or line.startswith('SKILLS ASSESSMENT:'):
                try:
                    result['skills_score'] = int(line.split(':')[1].strip().split()[0])
                except (ValueError, IndexError):
                    pass
                current_section = 'skills'

            elif line.startswith('EXPERIENCE ASSESSMENT:'):
                try:
                    result['experience_score'] = int(line.split(':')[1].strip().split()[0])
                except (ValueError, IndexError):
                    pass
                current_section = 'experience'

            elif line.startswith('EDUCATION ASSESSMENT:'):
                try:
                    result['education_score'] = int(line.split(':')[1].strip().split()[0])
                except (ValueError, IndexError):
                    pass
                current_section = 'education'

            elif line.startswith('STRENGTHS:'):
                current_section = 'strengths'
                result['strengths'] = []

            elif line.startswith('GAPS & CONCERNS:') or line.startswith('WEAKNESSES/GAPS:'):
                current_section = 'weaknesses'
                result['weaknesses'] = []

            elif line.startswith('INTERVIEW QUESTIONS:'):
                current_section = 'interview_questions'
                result['interview_questions'] = []

            elif line.startswith('SUMMARY:'):
                current_section = 'summary'
                result['summary'] = ''

            else:
                if line and current_section:
                    if current_section == 'strengths':
                        if line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                            result['strengths'].append(line.lstrip('-•123456789. ').strip())
                    elif current_section == 'weaknesses':
                        if line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                            result['weaknesses'].append(line.lstrip('-•123456789. ').strip())
                    elif current_section == 'interview_questions':
                        if line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.'):
                            result['interview_questions'].append(line.lstrip('-•123456789. ').strip())
                    elif current_section == 'summary':
                        result['summary'] += line + ' '

        result['summary'] = result['summary'].strip()

        return result
