# pdf-to-image

A web application that converts a PDF document into a ZIP archive of JPG images. Each page of the PDF becomes a separate high-resolution JPEG file (500 DPI).

## Technologies

- Python 3.10
- Flask + Gunicorn
- Pillow / NumPy
- Poppler (`pdftoppm`)
- Docker

## Project Structure

```
app/
  app.py              # Flask app with upload and conversion endpoints
  doc.py              # PDF-to-JPEG conversion logic via pdftoppm
  gunicorn_config.py  # Gunicorn settings (4 workers, port 5000, 1hr timeout)
  helper.py           # Utility functions
  wsgi.py             # WSGI entry point
  requirements.txt    # Python dependencies
Dockerfile            # Builds the container image
```

## Local Setup

1. Install [Docker](https://docs.docker.com/get-docker/).
2. Build the image:
   ```
   docker build -t pdf-to-image .
   ```
3. Run the container:
   ```
   docker run -p 5000:5000 pdf-to-image
   ```

## Using the Application

1. Visit [http://localhost:5000](http://localhost:5000).
2. Click **Browse** and select a PDF file.
3. Click **Submit** to upload and convert the PDF.
4. A ZIP file will automatically download once conversion is complete.
5. Unzip the archive to access the JPG images — one image per PDF page.

## How It Works

The app accepts a PDF upload via a multipart form POST to `/api`. It saves the file to a temporary directory, invokes `pdftoppm` (from Poppler) at 500 DPI to render each page as a JPEG, packages the images into a ZIP archive, and streams it back to the browser as a download. The temporary directory is cleaned up automatically after the response is sent.
