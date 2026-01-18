import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

from resume_parser import ResumeParser
from ai_analyzer import AIAnalyzer


class ResumeScreeningApp:
    """Main application for resume screening."""

    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Screening Assistant")
        self.root.geometry("1200x800")

        self.resumes = []
        self.analysis_results = []
        self.analyzer = None

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: Criteria and Upload
        self.tab_criteria = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_criteria, text="Criteria & Upload")

        # Tab 2: Results
        self.tab_results = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_results, text="Results")

        # Tab 3: Comparison
        self.tab_comparison = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_comparison, text="Comparison")

        self.setup_criteria_tab()
        self.setup_results_tab()
        self.setup_comparison_tab()

        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_criteria_tab(self):
        """Set up the criteria and upload tab."""
        frame = ttk.Frame(self.tab_criteria, padding="20")
        frame.pack(fill='both', expand=True)

        # API Key Section
        api_frame = ttk.LabelFrame(frame, text="API Configuration", padding="10")
        api_frame.pack(fill='x', pady=(0, 10))

        # AI Provider Selection
        ttk.Label(api_frame, text="AI Provider:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.provider_var = tk.StringVar(value="anthropic")
        provider_frame = ttk.Frame(api_frame)
        provider_frame.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)

        ttk.Radiobutton(
            provider_frame,
            text="Anthropic (Claude)",
            variable=self.provider_var,
            value="anthropic",
            command=self.toggle_provider
        ).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            provider_frame,
            text="OpenAI (GPT)",
            variable=self.provider_var,
            value="openai",
            command=self.toggle_provider
        ).pack(side=tk.LEFT, padx=5)

        # API Key Input
        ttk.Label(api_frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(api_frame, width=50, show="*")
        self.api_key_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)

        api_frame.columnconfigure(1, weight=1)

        # Analysis Mode Section
        mode_frame = ttk.LabelFrame(frame, text="Analysis Mode", padding="10")
        mode_frame.pack(fill='x', pady=(0, 10))

        self.analysis_mode = tk.StringVar(value="description")
        ttk.Radiobutton(
            mode_frame,
            text="Compare with Job Description (Recommended)",
            variable=self.analysis_mode,
            value="description",
            command=self.toggle_analysis_mode
        ).pack(anchor=tk.W, pady=2)

        ttk.Radiobutton(
            mode_frame,
            text="Use Custom Criteria",
            variable=self.analysis_mode,
            value="criteria",
            command=self.toggle_analysis_mode
        ).pack(anchor=tk.W, pady=2)

        # Job Description Section
        self.jd_frame = ttk.LabelFrame(frame, text="Job Description", padding="10")
        self.jd_frame.pack(fill='both', expand=True, pady=(0, 10))

        ttk.Label(
            self.jd_frame,
            text="Paste the complete job description here. The AI will analyze resumes against this JD.",
            font=('Arial', 9)
        ).pack(anchor=tk.W, pady=(0, 5))

        self.job_description_text = scrolledtext.ScrolledText(
            self.jd_frame,
            wrap=tk.WORD,
            height=12
        )
        self.job_description_text.pack(fill='both', expand=True)

        # Custom Criteria Section (initially hidden)
        self.criteria_frame = ttk.LabelFrame(frame, text="Custom Screening Criteria", padding="10")
        # Don't pack yet - will be shown based on mode

        # Job Title
        ttk.Label(self.criteria_frame, text="Job Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.job_title_entry = ttk.Entry(self.criteria_frame, width=50)
        self.job_title_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)

        # Skills
        ttk.Label(self.criteria_frame, text="Required Skills (comma-separated):").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.skills_text = tk.Text(self.criteria_frame, width=50, height=4)
        self.skills_text.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)

        # Experience
        ttk.Label(self.criteria_frame, text="Experience Level:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.experience_entry = ttk.Entry(self.criteria_frame, width=50)
        self.experience_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)

        # Education
        ttk.Label(self.criteria_frame, text="Education Requirements:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.education_entry = ttk.Entry(self.criteria_frame, width=50)
        self.education_entry.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)

        # Additional Notes
        ttk.Label(self.criteria_frame, text="Additional Notes:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        self.notes_text = tk.Text(self.criteria_frame, width=50, height=3)
        self.notes_text.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=5)

        self.criteria_frame.columnconfigure(1, weight=1)

        # Upload Section
        upload_frame = ttk.LabelFrame(frame, text="Upload Resumes", padding="10")
        upload_frame.pack(fill='x', pady=(0, 10))

        self.uploaded_files_label = ttk.Label(upload_frame, text="No files selected")
        self.uploaded_files_label.pack(pady=5)

        ttk.Button(upload_frame, text="Select Resume Files", command=self.select_files).pack(pady=5)

        # Analyze Button
        ttk.Button(frame, text="Analyze Resumes", command=self.start_analysis).pack(fill='x', pady=10)

    def setup_results_tab(self):
        """Set up the results tab."""
        frame = ttk.Frame(self.tab_results, padding="20")
        frame.pack(fill='both', expand=True)

        # Results table
        columns = ('Rank', 'Name', 'Score', 'Skills', 'Experience', 'Education', 'Recommendation')
        self.results_tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_tree.bind('<<TreeviewSelect>>', self.on_result_select)

        # Details panel
        details_frame = ttk.LabelFrame(frame, text="Candidate Details", padding="10")
        details_frame.pack(fill='both', expand=True, pady=(10, 0))

        self.details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, height=12)
        self.details_text.pack(fill='both', expand=True)

        # Export button
        ttk.Button(frame, text="Export to Excel", command=self.export_to_excel).pack(fill='x', pady=(10, 0))

    def setup_comparison_tab(self):
        """Set up the comparison tab."""
        frame = ttk.Frame(self.tab_comparison, padding="20")
        frame.pack(fill='both', expand=True)

        instruction_label = ttk.Label(
            frame,
            text="Select candidates in the Results tab to compare them side-by-side here",
            font=('Arial', 10)
        )
        instruction_label.pack(pady=10)

        self.comparison_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=25)
        self.comparison_text.pack(fill='both', expand=True)

    def select_files(self):
        """Open file dialog to select resume files."""
        files = filedialog.askopenfilenames(
            title="Select Resume Files",
            filetypes=[
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx *.doc"),
                ("All Files", "*.*")
            ]
        )

        if files:
            self.resumes = list(files)
            self.uploaded_files_label.config(text=f"{len(files)} file(s) selected")

    def start_analysis(self):
        """Start the resume analysis process."""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter your API key")
            return

        if not self.resumes:
            messagebox.showerror("Error", "Please select at least one resume file")
            return

        # Get criteria based on analysis mode
        mode = self.analysis_mode.get()

        if mode == "description":
            job_description = self.job_description_text.get("1.0", tk.END).strip()
            if not job_description:
                messagebox.showerror("Error", "Please enter a job description")
                return

            criteria = {
                'job_description': job_description
            }
        else:
            criteria = {
                'job_title': self.job_title_entry.get().strip(),
                'skills': self.skills_text.get("1.0", tk.END).strip(),
                'experience': self.experience_entry.get().strip(),
                'education': self.education_entry.get().strip(),
                'additional_notes': self.notes_text.get("1.0", tk.END).strip()
            }

            if not criteria['job_title']:
                messagebox.showerror("Error", "Please enter a job title")
                return

        provider = self.provider_var.get()

        # Disable button and show progress
        self.status_bar.config(text="Analyzing resumes... Please wait")
        self.root.update()

        # Run analysis in thread
        thread = threading.Thread(target=self.analyze_resumes, args=(api_key, criteria, provider))
        thread.start()

    def analyze_resumes(self, api_key: str, criteria: Dict[str, Any], provider: str):
        """Analyze all resumes (runs in background thread)."""
        try:
            self.analyzer = AIAnalyzer(api_key, provider)
            parser = ResumeParser()
            self.analysis_results = []

            for i, resume_path in enumerate(self.resumes, 1):
                self.root.after(0, lambda idx=i: self.status_bar.config(
                    text=f"Analyzing resume {idx}/{len(self.resumes)}..."
                ))

                # Parse resume
                resume_text = parser.parse_resume(resume_path)
                if not resume_text:
                    continue

                # Analyze with AI
                result = self.analyzer.analyze_resume(resume_text, criteria)

                # Add metadata
                result['filename'] = os.path.basename(resume_path)
                result['filepath'] = resume_path

                self.analysis_results.append(result)

            # Sort by score
            self.analysis_results.sort(key=lambda x: x.get('overall_score', 0), reverse=True)

            # Update UI on main thread
            self.root.after(0, self.display_results)
            self.root.after(0, lambda: self.status_bar.config(
                text=f"Analysis complete! {len(self.analysis_results)} resumes analyzed"
            ))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.status_bar.config(text="Analysis failed"))

    def display_results(self):
        """Display analysis results in the results table."""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Add results
        for rank, result in enumerate(self.analysis_results, 1):
            self.results_tree.insert('', tk.END, values=(
                rank,
                result.get('filename', 'Unknown'),
                f"{result.get('overall_score', 0)}%",
                f"{result.get('skills_score', 0)}%",
                f"{result.get('experience_score', 0)}%",
                f"{result.get('education_score', 0)}%",
                result.get('recommendation', 'N/A')
            ))

    def on_result_select(self, event):
        """Handle result selection."""
        selection = self.results_tree.selection()
        if not selection:
            return

        # Clear details
        self.details_text.delete("1.0", tk.END)

        # Show details for selected candidates
        details = []
        for item in selection:
            idx = self.results_tree.index(item)
            result = self.analysis_results[idx]

            detail = f"""
{'='*60}
Candidate: {result.get('filename', 'Unknown')}
Overall Score: {result.get('overall_score', 0)}%
Interview Recommendation: {result.get('interview_recommendation', result.get('recommendation', 'N/A'))}

{'='*60}
STRENGTHS:
"""
            for strength in result.get('strengths', []):
                detail += f"  • {strength}\n"

            detail += f"\nGAPS & CONCERNS:\n"
            for weakness in result.get('weaknesses', []):
                detail += f"  • {weakness}\n"

            # Add interview questions if available
            if result.get('interview_questions'):
                detail += f"\nSUGGESTED INTERVIEW QUESTIONS:\n"
                for q in result.get('interview_questions', []):
                    detail += f"  • {q}\n"

            detail += f"\nSUMMARY:\n{result.get('summary', 'No summary available')}\n"
            detail += f"\n{'='*60}\n"

            details.append(detail)

        self.details_text.insert("1.0", "\n".join(details))

        # Update comparison tab
        self.update_comparison_tab()

    def toggle_provider(self):
        """Handle AI provider toggle."""
        pass  # Just updates the selection for use in analysis

    def toggle_analysis_mode(self):
        """Toggle between job description and custom criteria mode."""
        mode = self.analysis_mode.get()

        if mode == "description":
            # Show job description, hide custom criteria
            self.jd_frame.pack(fill='both', expand=True, pady=(0, 10))
            self.criteria_frame.pack_forget()
        else:
            # Show custom criteria, hide job description
            self.jd_frame.pack_forget()
            self.criteria_frame.pack(fill='both', expand=True, pady=(0, 10))

    def update_comparison_tab(self):
        """Update the comparison tab with selected candidates."""
        selection = self.results_tree.selection()
        if not selection:
            return

        comparison = "CANDIDATE COMPARISON\n" + "="*80 + "\n\n"

        for item in selection:
            idx = self.results_tree.index(item)
            result = self.analysis_results[idx]

            comparison += f"CANDIDATE: {result.get('filename', 'Unknown')}\n"
            comparison += f"Overall Score: {result.get('overall_score', 0)}%\n"
            comparison += f"Skills: {result.get('skills_score', 0)}% | "
            comparison += f"Experience: {result.get('experience_score', 0)}% | "
            comparison += f"Education: {result.get('education_score', 0)}%\n"
            comparison += f"Recommendation: {result.get('recommendation', 'N/A')}\n"
            comparison += f"Summary: {result.get('summary', 'N/A')}\n"
            comparison += "-"*80 + "\n\n"

        self.comparison_text.delete("1.0", tk.END)
        self.comparison_text.insert("1.0", comparison)

    def export_to_excel(self):
        """Export results to Excel file."""
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No results to export")
            return

        # Prepare data
        data = []
        for result in self.analysis_results:
            data.append({
                'Rank': 0,  # Will be filled
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

        # Add rank
        for i, row in enumerate(data, 1):
            row['Rank'] = i

        df = pd.DataFrame(data)

        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"resume_screening_results_{timestamp}.xlsx"

        filepath = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".xlsx",
            initialfile=default_filename,
            filetypes=[("Excel Files", "*.xlsx")]
        )

        if filepath:
            try:
                df.to_excel(filepath, index=False)
                messagebox.showinfo("Success", f"Results exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = ResumeScreeningApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
