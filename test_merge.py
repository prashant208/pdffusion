import requests
import os

def test_merge():
    url = "http://127.0.0.1:5000/"
    files = [
        ('pdfs', ('dummy1.pdf', open('dummy1.pdf', 'rb'), 'application/pdf')),
        ('pdfs', ('dummy2.pdf', open('dummy2.pdf', 'rb'), 'application/pdf'))
    ]
    
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        with open('merged_output.pdf', 'wb') as f:
            f.write(response.content)
        print("Success: Merged PDF saved as merged_output.pdf")
        
        # Simple check if it looks like a PDF
        with open('merged_output.pdf', 'rb') as f:
            header = f.read(4)
            if header == b'%PDF':
                print("Verification: Output file has PDF header.")
            else:
                print("Verification Failed: Output file does not have PDF header.")
    else:
        print(f"Failed: Status Code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_merge()
