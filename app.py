from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdfs' not in request.files:
            return "No files uploaded", 400
        
        files = request.files.getlist('pdfs')
        ranges = request.form.getlist('ranges')
        
        if not files or files[0].filename == '':
            return "No selected files", 400

        # If ranges aren't provided (e.g. old form submit), default to 'all'
        if not ranges:
            ranges = ['all'] * len(files)

        from PyPDF2 import PdfWriter, PdfReader
        writer = PdfWriter()
        
        try:
            for i, pdf_file in enumerate(files):
                reader = PdfReader(pdf_file)
                num_pages = len(reader.pages)
                
                # Parse range for this file
                range_str = ranges[i] if i < len(ranges) else 'all'
                pages_to_add = parse_page_range(range_str, num_pages)
                
                for page_num in pages_to_add:
                    writer.add_page(reader.pages[page_num])
            
            output_buffer = io.BytesIO()
            writer.write(output_buffer)
            writer.close()
            output_buffer.seek(0)
            
            return send_file(
                output_buffer,
                as_attachment=True,
                download_name='merged.pdf',
                mimetype='application/pdf'
            )
        except Exception as e:
            return str(e), 500

    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/rotate', methods=['GET', 'POST'])
def rotate():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['pdf']
        if file.filename == '':
            return "No selected file", 400
            
        angle = int(request.form.get('angle', 90))
        
        from PyPDF2 import PdfReader, PdfWriter
        reader = PdfReader(file)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.rotate(angle)
            writer.add_page(page)
            
        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        writer.close()
        output_buffer.seek(0)
        
        return send_file(
            output_buffer,
            as_attachment=True,
            download_name=f'rotated_{angle}.pdf',
            mimetype='application/pdf'
        )

    return render_template('rotate.html')

@app.route('/split', methods=['GET', 'POST'])
def split():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['pdf']
        range_str = request.form.get('range', '')
        
        if file.filename == '':
            return "No selected file", 400
            
        from PyPDF2 import PdfReader, PdfWriter
        reader = PdfReader(file)
        writer = PdfWriter()
        
        num_pages = len(reader.pages)
        pages_to_keep = parse_page_range(range_str, num_pages)
        
        for page_num in pages_to_keep:
            writer.add_page(reader.pages[page_num])
            
        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        writer.close()
        output_buffer.seek(0)
        
        return send_file(
            output_buffer,
            as_attachment=True,
            download_name='split_selection.pdf',
            mimetype='application/pdf'
        )

    return render_template('split.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

def parse_page_range(range_str, max_pages):
    """
    Parses a page range string into a list of 0-based page indices.
    Examples: "all", "1-3, 5", "2-end"
    """
    range_str = range_str.lower().strip()
    if not range_str or range_str == 'all':
        return list(range(max_pages))
    
    pages = set()
    parts = range_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = part.split('-')
                start = int(start) if start else 1
                if end == 'end':
                    end = max_pages
                else:
                    end = int(end) if end else max_pages
                
                # Adjust to 0-based, inclusive of end
                start = max(1, start) - 1
                end = min(max_pages, end)
                
                for p in range(start, end):
                    pages.add(p)
            except ValueError:
                continue # Ignore malformed ranges
        else:
            try:
                page = int(part)
                # Adjust to 0-based
                page = max(1, page) - 1
                if 0 <= page < max_pages:
                    pages.add(page)
            except ValueError:
                continue

    return sorted(list(pages))

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # In production, debug should be False. You might want to toggle this with an env var too.
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
