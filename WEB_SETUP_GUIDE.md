# Resume Screening Web Application

A modern web-based resume screening application powered by AI, accessible from any browser on your local network.

## Features

- 🌐 **Web-based Interface** - Access from any browser on your network
- 🔒 **Password Protected** - Simple password authentication
- 🤖 **AI-Powered Analysis** - Choose between Anthropic (Claude) or OpenAI (GPT)
- 📝 **Job Description Comparison** - Compare resumes against full job descriptions
- 📊 **Visual Results** - Beautiful Bootstrap 5 interface
- 📥 **Excel Export** - Download results for further analysis
- 🎯 **Interview Recommendations** - Get Yes/No/Maybe recommendations with suggested questions

## Installation

### 1. Install Dependencies

```bash
cd Resume_screening
pip install -r requirements.txt
```

### 2. Set Password (Optional)

By default, the password is `admin123`. To change it, set an environment variable:

**Mac/Linux:**
```bash
export APP_PASSWORD=your_secure_password
```

**Windows (Command Prompt):**
```cmd
set APP_PASSWORD=your_secure_password
```

**Windows (PowerShell):**
```powershell
$env:APP_PASSWORD="your_secure_password"
```

### 3. Run the Application

```bash
python app.py
```

The app will start at: **http://localhost:5000**

## Accessing from Other Devices

### Find Your IP Address

**Mac/Linux:**
```bash
ifconfig | grep "inet "
```

**Windows:**
```cmd
ipconfig
```

Look for the IPv4 address (e.g., `192.168.1.100`)

### Access from Other Devices

On other devices in your network, navigate to:
```
http://YOUR_IP_ADDRESS:5000
```

For example: `http://192.168.1.100:5000`

## Firewall Settings

If you can't access from other devices:

### Mac
1. System Preferences → Security & Privacy → Firewall
2. Allow Python or your terminal app

### Windows
1. Windows Defender Firewall → Advanced Settings
2. Inbound Rules → New Rule
3. Select "Port" → TCP → Specific local ports: 5000
4. Allow the connection

## Usage

### 1. Login
- Open the app in your browser
- Enter the password (default: `admin123`)

### 2. Configure API
- Select AI Provider: Anthropic (Claude) or OpenAI (GPT)
- Enter your API key

### 3. Choose Analysis Mode

**Option A: Job Description (Recommended)**
- Paste the complete job description
- AI analyzes resumes against the full JD

**Option B: Custom Criteria**
- Fill in job title, skills, experience, education
- AI analyzes based on these criteria

### 4. Upload Resumes
- Click "Choose Files" or drag and drop
- Select PDF or DOCX files
- Click "Analyze Resumes"

### 5. Review Results
- Candidates ranked by score (0-100%)
- Color-coded badges: Green (80%+), Yellow (60-79%), Red (<60%)
- Interview recommendations: Yes/No/Maybe
- Click "View Details" for full analysis:
  - Strengths
  - Gaps & Concerns
  - Suggested interview questions
  - Summary

### 6. Export Results
- Click "Export to Excel"
- Results downloaded as `.xlsx` file

## Features Breakdown

### Analysis Results
- **Overall Score**: Total match score (0-100%)
- **Interview Recommendation**: Yes/No/Maybe
- **Category Scores**: Skills, Experience, Education
- **Strengths**: What makes them a good fit
- **Gaps**: What they're missing
- **Interview Questions**: AI-generated questions based on gaps
- **Summary**: Why they should/shouldn't be interviewed

### Export Format
Excel file includes:
- Rank
- Filename
- Overall Score
- Interview Recommendation
- Skills, Experience, Education scores
- Strengths
- Gaps & Concerns
- Interview Questions
- Summary

## Security

### Production Deployment
For production use, you should:

1. **Set a strong password:**
   ```bash
   export APP_PASSWORD=your_secure_password
   ```

2. **Set a secret key:**
   ```bash
   export FLASK_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   ```

3. **Disable debug mode** (in `app.py`, change last line to):
   ```python
   app.run(host='0.0.0.0', port=5000, debug=False)
   ```

4. **Use HTTPS** (consider using nginx as reverse proxy)

## Troubleshooting

**"Connection refused" error:**
- Check if the app is running
- Verify the IP address and port (5000)
- Check firewall settings

**"Authentication required" error:**
- Session expired, login again
- Clear browser cookies

**Files not uploading:**
- Check file size (max 16MB)
- Verify file format (PDF or DOCX only)
- Check upload folder permissions

**API errors:**
- Verify API key is correct
- Check you have credits available
- Try switching AI provider

**Slow performance:**
- Analysis speed depends on AI provider response time
- Large job descriptions may take longer
- Multiple resumes are processed sequentially

## Architecture

```
Resume_screening/
├── app.py                 # Flask web application
├── resume_parser.py       # Resume text extraction
├── ai_analyzer.py         # AI analysis engine
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── login.html       # Login page
│   └── index.html       # Main application
└── uploads/             # Temporary file storage (auto-created)
```

## Cost Considerations

- **Anthropic Claude**: ~$0.15-0.30 per resume
- **OpenAI GPT-4o**: ~$0.10-0.25 per resume
- Both offer free credits for new accounts

## Browser Support

Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

## Performance Tips

1. **Batch Processing**: Upload multiple resumes at once
2. **Job Description Mode**: More accurate than custom criteria
3. **Specific Descriptions**: Detailed JDs yield better results
4. **Network**: Use wired connection for faster uploads

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in browser console (F12)
3. Check terminal output for server errors
