from flask import Flask, render_template, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
from functools import wraps

from resume_parser import ResumeParser
from ai_analyzer import AIAnalyzer

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
PASSWORD = os.environ.get('APP_PASSWORD', 'admin123')  # Change this password!

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render login page or main app."""
    if session.get('logged_in'):
        return render_template('index.html')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Handle login request."""
    password = request.json.get('password')
    if password == PASSWORD:
        session['logged_in'] = True
        session.permanent = True
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid password'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    """Handle logout request."""
    session.pop('logged_in', None)
    return jsonify({'success': True})


# Serve PWA manifest
@app.route('/static/manifest.json')
def serve_manifest():
    """Serve the PWA manifest file."""
    return send_file('static/manifest.json', mimetype='application/manifest+json')


# Serve service worker at root
@app.route('/service-worker.js')
def serve_service_worker():
    """Serve the service worker file."""
    response = send_file('service-worker.js', mimetype='application/javascript')
    response.headers['Service-Worker-Allowed'] = '/'
    return response


@app.route('/api/upload', methods=['POST'])
@login_required
def upload_files():
    """Handle file uploads."""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    uploaded_files = []

    for file in files:
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            uploaded_files.append({
                'original_name': filename,
                'saved_path': filepath,
                'id': unique_filename
            })

    return jsonify({
        'success': True,
        'files': uploaded_files,
        'count': len(uploaded_files)
    })


@app.route('/api/analyze', methods=['POST'])
@login_required
def analyze():
    """Analyze resumes against criteria."""
    data = request.json

    # Validate request
    if not data.get('api_key'):
        return jsonify({'error': 'API key is required'}), 400

    if not data.get('files'):
        return jsonify({'error': 'No files to analyze'}), 400

    # Get analysis mode and criteria
    mode = data.get('mode', 'criteria')

    if mode == 'description':
        job_description = data.get('job_description', '').strip()
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        criteria = {'job_description': job_description}
    else:
        job_title = data.get('job_title', '').strip()
        if not job_title:
            return jsonify({'error': 'Job title is required'}), 400
        criteria = {
            'job_title': job_title,
            'skills': data.get('skills', ''),
            'experience': data.get('experience', ''),
            'education': data.get('education', ''),
            'additional_notes': data.get('additional_notes', '')
        }

    provider = data.get('provider', 'anthropic')

    try:
        # Initialize analyzer
        analyzer = AIAnalyzer(data['api_key'], provider)
        parser = ResumeParser()
        results = []

        # Analyze each file
        for file_info in data['files']:
            try:
                # Parse resume
                resume_text = parser.parse_resume(file_info['saved_path'])
                if not resume_text:
                    results.append({
                        'filename': file_info['original_name'],
                        'error': 'Failed to parse resume'
                    })
                    continue

                # Analyze with AI
                analysis = analyzer.analyze_resume(resume_text, criteria)
                analysis['filename'] = file_info['original_name']
                results.append(analysis)

            except Exception as e:
                results.append({
                    'filename': file_info['original_name'],
                    'error': str(e)
                })

        # Sort by score
        valid_results = [r for r in results if 'error' not in r]
        valid_results.sort(key=lambda x: x.get('overall_score', 0), reverse=True)

        # Put errors at the end
        error_results = [r for r in results if 'error' in r]
        final_results = valid_results + error_results

        # Clean up uploaded files
        for file_info in data['files']:
            try:
                if os.path.exists(file_info['saved_path']):
                    os.remove(file_info['saved_path'])
            except:
                pass

        return jsonify({
            'success': True,
            'results': final_results,
            'analyzed': len(valid_results),
            'errors': len(error_results)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['POST'])
@login_required
def export_results():
    """Export results to Excel."""
    import pandas as pd

    data = request.json
    results = data.get('results', [])

    if not results:
        return jsonify({'error': 'No results to export'}), 400

    # Prepare data
    export_data = []
    for rank, result in enumerate(results, 1):
        if 'error' not in result:
            export_data.append({
                'Rank': rank,
                'Filename': result.get('filename', 'Unknown'),
                'Overall Score': result.get('overall_score', 0),
                'Interview Recommendation': result.get('interview_recommendation', result.get('recommendation', 'N/A')),
                'Skills Score': result.get('skills_score', 0),
                'Experience Score': result.get('experience_score', 0),
                'Education Score': result.get('education_score', 0),
                'Qualifications Score': result.get('qualifications_score', 0),
                'Strengths': '; '.join(result.get('strengths', [])),
                'Gaps & Concerns': '; '.join(result.get('weaknesses', [])),
                'Interview Questions': '; '.join(result.get('interview_questions', [])),
                'Summary': result.get('summary', '')
            })

    # Create Excel file
    df = pd.DataFrame(export_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resume_screening_results_{timestamp}.xlsx"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df.to_excel(filepath, index=False)

    # Send file and clean up
    try:
        return send_file(filepath, as_attachment=True, download_name=filename)
    finally:
        import threading
        def cleanup():
            import time
            time.sleep(5)  # Wait 5 seconds before cleanup
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
        threading.Thread(target=cleanup).start()


if __name__ == '__main__':
    # Run on all network interfaces for local network access
    app.run(host='0.0.0.0', port=5000, debug=True)
