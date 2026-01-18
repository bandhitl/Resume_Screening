# Setup Guide - Resume Screening Application

## Installation

1. **Install Python 3.8 or higher**

2. **Install dependencies:**
   ```bash
   cd Resume_screening
   pip install -r requirements.txt
   ```

## API Key Setup

### Option 1: Using Anthropic (Claude)

1. Get your API key from https://www.anthropic.com/
2. Create a `.env` file in the project directory
3. Add your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

### Option 2: Using OpenAI (GPT)

1. Get your API key from https://platform.openai.com/api-keys
2. Create a `.env` file in the project directory (or edit existing)
3. Add your key:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

### Option 3: Using Both

You can add both keys to your `.env` file and switch between them in the app:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-proj-your-key-here
```

## Running the Application

```bash
python resume_screener.py
```

## How to Use

### Method 1: Compare with Job Description (Recommended)

1. Select your AI provider (Anthropic or OpenAI)
2. Enter your API key
3. Select "Compare with Job Description"
4. Paste the complete job description in the text box
5. Upload resume files (PDF or DOCX)
6. Click "Analyze Resumes"
7. Review results:
   - **Overall Score**: How well the candidate matches (0-100%)
   - **Interview Recommendation**: Yes/No/Maybe
   - **Detailed Analysis**: Strengths, gaps, and suggested interview questions

### Method 2: Use Custom Criteria

1. Select your AI provider (Anthropic or OpenAI)
2. Enter your API key
3. Select "Use Custom Criteria"
4. Fill in:
   - Job Title
   - Required Skills (comma-separated)
   - Experience Level
   - Education Requirements
   - Additional Notes
5. Upload resume files
6. Click "Analyze Resumes"

## Understanding Results

### Scores
- **Overall Score (0-100)**: Total match score
- **Skills Score**: How well skills match requirements
- **Experience Score**: Experience level match
- **Education Score**: Education requirements match
- **Qualifications Score**: Overall qualifications match (JD mode only)

### Interview Recommendations
- **Yes**: Strong candidate, recommend interview
- **Maybe**: Potential candidate, interview to learn more
- **No**: Not a good fit for this role

### Features
- **Candidate Ranking**: Automatically sorted by score
- **Side-by-Side Comparison**: Compare multiple candidates
- **Interview Questions**: AI-generated questions based on resume gaps
- **Export to Excel**: Save all results for further review

## Tips for Best Results

1. **Use Job Description Mode**: More accurate than custom criteria
2. **Be Specific**: Detailed job descriptions yield better analysis
3. **Review Interview Questions**: Use AI-generated questions in interviews
4. **Check Gaps**: Look at the "Gaps & Concerns" section for missing qualifications
5. **Compare Top Candidates**: Use the Comparison tab to view top candidates side-by-side

## Troubleshooting

**"API key not found" error:**
- Make sure you've created a `.env` file
- Check that the API key is correct
- Or enter the key directly in the app

**"Failed to analyze resume" error:**
- Check your internet connection
- Verify your API key has credits available
- Try the other AI provider

**PDF not parsing correctly:**
- Try converting to DOCX format
- Ensure the PDF is text-based (not scanned images)

## Cost Considerations

- **Anthropic Claude**: ~$0.15-0.30 per resume analysis
- **OpenAI GPT-4o**: ~$0.10-0.25 per resume analysis
- Cost varies based on resume length and job description complexity
- Both providers offer free credits for new accounts

## File Support

- **PDF**: .pdf files (text-based)
- **Word**: .docx, .doc files
- **Batch**: Upload multiple files at once

## Data Privacy

- Resumes are processed by the AI provider you choose
- Data is not stored permanently by the application
- Review your AI provider's privacy policy for details
