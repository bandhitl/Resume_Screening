# Resume Screening Application

A Python desktop application for HR professionals to screen resumes using AI-powered analysis.

## Features

- **Resume Upload**: Support for PDF and DOCX formats
- **AI-Powered Analysis**: Uses Claude AI to analyze and score resumes
- **Custom Screening Criteria**: Define job requirements, skills, experience levels
- **Candidate Ranking**: Automatic scoring and ranking based on criteria
- **Side-by-Side Comparison**: Compare multiple candidates easily
- **Export Results**: Export results to Excel

## Installation

1. Install Python 3.8 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Anthropic API key:
   - Create a file named `.env` in the project directory
   - Add your API key: `ANTHROPIC_API_KEY=your_api_key_here`

## Usage

Run the application:
```bash
python resume_screener.py
```

## How It Works

1. **Define Screening Criteria**: Enter job title, required skills, experience level, education
2. **Upload Resumes**: Select one or more resume files (PDF/DOCX)
3. **AI Analysis**: The app uses Claude AI to analyze each resume against criteria
4. **Review Results**: View scored candidates with detailed analysis
5. **Export**: Save results to Excel for further review

## Requirements

- Python 3.8+
- Anthropic API key (get one at https://www.anthropic.com/)
- Resume files in PDF or DOCX format
