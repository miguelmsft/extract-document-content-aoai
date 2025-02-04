# Extract Document RFP Content with Azure OpenAI  
   
This repository provides a Python script to extract structured information from PDF documents using Azure OpenAI's Document Intelligence capabilities. The script processes PDF files, converts each page into an image, and then uses Azure OpenAI to extract specific information from each page based on a custom prompt. The extracted information is saved as structured JSON files.  
   
## Table of Contents  
   
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Setup Instructions](#setup-instructions)  
- [Usage](#usage)  
- [Example Output](#example-output)  
- [Directory Structure](#directory-structure)  
- [License](#license)  
   
## Features  
   
- Converts PDF pages to high-resolution PNG images.  
- Utilizes Azure OpenAI to extract structured data from document images.  
- Customizable prompt to tailor the extraction process.  
- Saves extracted information in JSON format for easy consumption.  
- Handles multi-page PDF documents efficiently.  
   
## Prerequisites  
   
- **Python 3.8 or higher**  
- Azure account with an Azure OpenAI resource.  
- The following Python packages:  
  - `azure-openai`  
  - `python-dotenv`  
  - `pydantic`  
  - `PyMuPDF` (also known as `fitz`)  
  - `base64`  
  - `os`  
  - `json`  
  - `pathlib`  
   
## Setup Instructions  
   
### 1. Clone the Repository  
   
```bash  
git clone https://github.com/yourusername/extract-document-content-aoai.git  
cd extract-document-content-aoai  
```  
   
### 2. Install Dependencies  
   
It's recommended to use a virtual environment:  
   
```bash  
python -m venv venv  
source venv/bin/activate  # On Windows use `venv\Scripts\activate`  
```  
   
Install the required packages:  
   
```bash  
pip install -r requirements.txt  
```  
   
> **Note:** If you don't have a `requirements.txt` file, you can install the packages individually:  
   
```bash  
pip install azure-openai python-dotenv pydantic PyMuPDF  
```  
   
### 3. Configure Azure OpenAI Credentials  
   
Create a `.env` file in the root directory and add your Azure OpenAI credentials:  
   
```bash  
AOAI_ENDPOINT=https://your-azure-openai-endpoint.openai.azure.com/  
AOAI_API_KEY=your-azure-openai-api-key  
AOAI_DEPLOYMENT=your-deployment-name  
```  
   
- **AOAI_ENDPOINT**: Your Azure OpenAI endpoint URL.  
- **AOAI_API_KEY**: Your Azure OpenAI API key.  
- **AOAI_DEPLOYMENT**: The name of your Azure OpenAI deployment.  
   
### 4. Prepare Input Documents  
   
Place the PDF documents you want to process into the `input_documents` directory.  
   
## Usage  
   
Run the script using the following command:  
   
```bash  
python extract_requirements.py  
```  
   
The script will:  
   
1. Iterate over each PDF file in the `input_documents` directory.  
2. Convert each page of the PDF into a PNG image and save it in `output_images`.  
3. Send each image to Azure OpenAI with a custom prompt to extract information.  
4. Receive the structured JSON response and save it in `output_results`.  
   
### Customizing the Prompt  
   
You can modify the `prompt` variable in `extract_requirements.py` to customize the information you want to extract from the documents.  
   
Example prompt:  
   
```python  
prompt = """ From the given document, extract:  
1) The page number. It will be at the bottom of the page.  
2) The Requirement ID and requirement text for each requirement.   
    The requirement ID will be on the left side of the page, and it will be in the format of a number followed by a dot followed by numbers (e.g., 2.3 or 3.7.9).  
    The requirement text will be on the center to right side of the page and may consist of one or more paragraphs of text. Include any lists (e.g., (a), (b), (c)) as part of the requirement text.  
    If, at the beginning of the page, you see requirement text paragraphs with no requirement ID next to them, for requirement ID write "See previous ID" and for requirement text write the text of the requirement.  
    If the requirement text includes a table, write the table in markdown format."""  
```  
   
### Output  
   
- **Images:** PNG images of each page are saved in the `output_images` directory.  
- **Extracted Data:** JSON files containing the extracted information are saved in the `output_results` directory.  
   
## Example Output  
   
Running the script will produce console output similar to the following:  
   
```  
Processing RFP_healthcare_example.pdf...  
Saved image to RFP_healthcare_example_page1.png  
Image size: 286846 bytes  
Image dimensions: 1224x1584  
Saved extracted information to RFP_healthcare_example_page1.json  
Saved image to RFP_healthcare_example_page2.png  
Image size: 275876 bytes  
Image dimensions: 1224x1584  
Saved extracted information to RFP_healthcare_example_page2.json  
...  
```  
   
### Sample Extracted JSON  
   
An example of the extracted JSON data:  
   
```json  
{  
  "pageNumber": 1,  
  "extractedText": [  
    {  
      "RequirementID": "1.1",  
      "RequirementText": "The system shall provide secure login functionality."  
    },  
    {  
      "RequirementID": "1.2",  
      "RequirementText": "The system shall allow users to reset their password."  
    }  
  ]  
}  
```  
   
## Directory Structure  
   
```  
extract-document-content-aoai  
├── .env  
├── .gitignore  
├── LICENSE  
├── README.md  
├── extract_requirements.py  
├── input_documents  
│   └── your_document.pdf  
├── output_images  
│   ├── your_document_page1.png  
│   ├── your_document_page2.png  
│   └── ...  
└── output_results  
    ├── your_document_page1.json  
    ├── your_document_page2.json  
    └── ...  
```  
   
- `input_documents`: Place your PDF files here.  
- `output_images`: Contains the generated PNG images of each page.  
- `output_results`: Contains the extracted information in JSON format.  
   
## License  
   
This project is licensed under the [MIT License](LICENSE).  
   
---  
   
If you encounter any issues or have questions, please open an issue on GitHub or contact the repository owner.