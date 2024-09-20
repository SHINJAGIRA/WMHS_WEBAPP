from pdf2image import convert_from_path

try:
    images = convert_from_path('path/to/your/test.pdf')
    print(f"Number of pages: {len(images)}")
except Exception as e:
    print(f"Failed to process PDF: {e}")
