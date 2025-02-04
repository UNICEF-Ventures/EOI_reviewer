from flask import Flask, render_template, request, send_file
import pandas as pd
from datetime import datetime
import os
import re

# Get the directory containing this file
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your-secret-key'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class ApplicationReviewer:
    def __init__(self):
        self.df = None
        self.comments = {}
        self.evaluations = {}
        self.current_index = 0
        self.evaluator = 'Vipul'

    def determine_open_source_status(self, row):
        open_source = str(row.get('Is your solution Open Source?', '')).strip()
        return 'open' if 'Yes' in open_source else 'willing'

    def load_excel(self, file):
        self.df = pd.read_excel(file)
        self.df = self.df[self.df['Tech Evaluator'].str.lower() == self.evaluator.lower()]

        # Add open source status
        self.df['open_source_status'] = self.df.apply(self.determine_open_source_status, axis=1)

        return len(self.df) > 0

    def get_current_application(self):
        if self.df is None or len(self.df) == 0 or self.current_index >= len(self.df):
            return None
        return self.df.iloc[self.current_index].to_dict()

    def save_review(self, comment, evaluation):
        self.comments[self.current_index] = comment
        self.evaluations[self.current_index] = evaluation

    def export_reviews(self):
        if self.df is None:
            return None

        reviews = []
        for idx in range(len(self.df)):
            row = self.df.iloc[idx].to_dict()
            row.update({
                'Evaluation': self.evaluations.get(idx, ''),
                'Comment': self.comments.get(idx, '')
            })
            reviews.append(row)

        df_reviews = pd.DataFrame(reviews)
        
        # Save backup with all columns including the new evaluations
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(app.config['UPLOAD_FOLDER'], f'evaluation_backup_{timestamp}.xlsx')
        df_reviews.to_excel(backup_path, index=False)

        # Create summary with relevant columns
        summary_cols = [
            'ID', 'Name of company:', 'In which country is your company legally registered?',
            'Which of the following is your solution addressing? (select all that apply)',
            'What need or challenge is your solution addressing in your local context?',
            'Describe the solution you are proposing and how it is solving the challenges you described in the previous question:',
            'How you are using the technology(ies)?',
            'Describe the results of your initial testing and prototyping (quantitative and qualitative):',
            'Provide a link to the GitHub or other open repository for your solution:',
            'What are your project targets/milestones for the next 12 months?:',
            'Who are your key partners and advisors (only list actual partners, write NA if non-existent)',
            'Provide an overview of the capital and other contributions to the project (capital, human resources, assets, other investments and loans)',
            'Upload the video to YouTube and provide the link in this response form:',
            'open_source_status',
            'Evaluation',
            'Comment'
        ]
        
        # Only create summary if all required columns exist
        available_cols = [col for col in summary_cols if col in df_reviews.columns]
        summary = df_reviews[available_cols].copy()
        
        filename = f'reviews_{timestamp}.xlsx'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        summary.to_excel(filepath, index=False)

        return filepath

    def get_current_evaluation(self):
        if self.df is None:
            return ''
        return self.evaluations.get(self.current_index, '')

    def get_current_comment(self):
        if self.df is None:
            return ''
        return self.comments.get(self.current_index, '')

reviewer = ApplicationReviewer()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                success = reviewer.load_excel(file)
                if not success:
                    return "No applications found for evaluator", 400
        elif 'export' in request.form:
            if reviewer.df is None:
                return "No data loaded to export", 400
            if 'comment' in request.form:
                reviewer.save_review(request.form['comment'], request.form.get('evaluation', ''))
            filepath = reviewer.export_reviews()
            if filepath:
                return send_file(filepath, as_attachment=True)
            return "No data to export", 400
        elif 'comment' in request.form:
            if reviewer.df is None:
                return "No data loaded", 400
            reviewer.save_review(request.form['comment'], request.form.get('evaluation', ''))
            if 'next' in request.form and reviewer.df is not None and reviewer.current_index < len(reviewer.df) - 1:
                reviewer.current_index += 1
            elif 'prev' in request.form and reviewer.df is not None and reviewer.current_index > 0:
                reviewer.current_index -= 1

    return render_template('review.html',
                         reviewer=reviewer,
                         app=reviewer.get_current_application(),
                         current=reviewer.current_index + 1 if reviewer.df is not None else 0,
                         total=len(reviewer.df) if reviewer.df is not None else 0,
                         evaluation=reviewer.get_current_evaluation(),
                         comment=reviewer.get_current_comment())

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
