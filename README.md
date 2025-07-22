# PDF Content & Structure Extractor

This project extracts structured content such as titles, headings, and outlines from PDF documents. It uses a combination of layout analysis and machine learning (via ONNX and Transformers) to intelligently identify and categorize text elements.

## Features

- **Title & Outline Extraction**: Identifies the document title and hierarchical headings (H1, H2, H3).
- **Layout-Aware Analysis**: Considers font size, boldness, and position to improve accuracy.
- **Machine Learning Powered**: Uses a pre-trained model to understand text semantics for better classification.
- **JSON Output**: Saves the extracted structure in a clean, readable JSON format.
- **Cross-Platform**: Includes setup and usage instructions for both macOS/Linux and Windows.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Aditya19110/pdf-scanner.git
cd pdf-scanner
```

### 2. Create and Activate a Virtual Environment

**On macOS/Linux:**

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

**On Windows:**

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\\venv\\Scripts\\activate
```

### 3. Install Dependencies

With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Download the Model

We have th necessary model files in a `model/` directory. Make sure the folder is in the correct sturcture given below:

```
model/
├── tokenizer/
│   ├── ... (tokenizer files)
└── model.onnx
```

## How to Run(Locally)

1.  **Place PDFs in the `input` folder.** If the folder doesn't exist, it will be created automatically.
2.  **Run the main script:**

    ```bash
    python main.py
    ```

3.  **Check the `output` folder.** The script will generate a `.json` file for each processed PDF, containing the extracted title and outline.

## Run with Docker

To run the project in a Dockerized environment:

1. **Build the Docker image**:

   ```bash
   docker build -t pdf-extractor .
   ```
2. **Run the Docker container (mount input and output folders)**:

```bash
    docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-extractor
```


## Created By

Aditya Kulkarni & Vedika Lohiya