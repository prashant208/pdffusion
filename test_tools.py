import requests
import os

# Configuration
BASE_URL = 'http://127.0.0.1:5000'
TEST_FILES_DIR = '.'

def test_rotate():
    print("\n--- Testing PDF Rotate ---")
    files = {'pdf': open('dummy1.pdf', 'rb')}
    data = {'angle': '90'}
    
    try:
        response = requests.post(f'{BASE_URL}/rotate', files=files, data=data)
        if response.status_code == 200:
            with open('rotated_test.pdf', 'wb') as f:
                f.write(response.content)
            print("✅ Rotate successful! Saved 'rotated_test.pdf'")
        else:
            print(f"❌ Rotate failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        files['pdf'].close()

def test_split():
    print("\n--- Testing PDF Split ---")
    # We need a multi-page PDF for split testing.
    # Assuming create_multipage_pdfs.py was run or we can use dummy1.pdf (single page) as a basic test.
    # Let's use 'dummy1.pdf' and just extract page 1 (index 0, so range '1')
    files = {'pdf': open('dummy1.pdf', 'rb')}
    data = {'range': '1'}
    
    try:
        response = requests.post(f'{BASE_URL}/split', files=files, data=data)
        if response.status_code == 200:
            with open('split_test.pdf', 'wb') as f:
                f.write(response.content)
            print("✅ Split successful! Saved 'split_test.pdf'")
        else:
            print(f"❌ Split failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        files['pdf'].close()

if __name__ == '__main__':
    # Ensure dummy file exists
    if not os.path.exists('dummy1.pdf'):
        print("Creating dummy PDF for testing...")
        from reportlab.pdfgen import canvas
        c = canvas.Canvas("dummy1.pdf")
        c.drawString(100, 750, "Hello World")
        c.save()

    test_rotate()
    test_split()
