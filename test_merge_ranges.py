import requests
import os
from PyPDF2 import PdfReader
import io

def test_merge_ranges():
    url = "http://127.0.0.1:5000/"
    
    # Files: multi1.pdf (5 pages), multi2.pdf (3 pages)
    # Goal: Doc 1 (Pages 1, 3-4 -> indices 0, 2, 3) + Doc 2 (All -> 3 pages)
    # Expected Total: 3 + 3 = 6 pages
    
    files = [
        ('pdfs', ('multi1.pdf', open('multi1.pdf', 'rb'), 'application/pdf')),
        ('pdfs', ('multi2.pdf', open('multi2.pdf', 'rb'), 'application/pdf'))
    ]
    
    # Ranges must correspond to the files order
    data = [
        ('ranges', '1, 3-4'), # For multi1.pdf (pages 1, 3, 4)
        ('ranges', 'all')     # For multi2.pdf (all 3 pages)
    ]
    
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        with open('merged_ranges.pdf', 'wb') as f:
            f.write(response.content)
        print("Success: Merged PDF saved as merged_ranges.pdf")
        
        # Verify page count
        reader = PdfReader('merged_ranges.pdf')
        num_pages = len(reader.pages)
        print(f"Verification: Output has {num_pages} pages.")
        
        expected_pages = 6
        if num_pages == expected_pages:
             print("Test PASSED: Page count matches.")
        else:
             print(f"Test FAILED: Expected {expected_pages}, got {num_pages}.")

    else:
        print(f"Failed: Status Code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_merge_ranges()
