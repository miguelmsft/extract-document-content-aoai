import base64  
import os  
import json  
from dotenv import load_dotenv  
from openai import AzureOpenAI  
from pydantic import BaseModel  
from pathlib import Path  
import fitz  # PyMuPDF  
  
# Load environment variables  
load_dotenv()  
  
# Azure OpenAI environment variables  
aoai_endpoint = os.getenv("AOAI_ENDPOINT")  
aoai_api_key = os.getenv("AOAI_API_KEY")  
aoai_deployment_name = os.getenv("AOAI_DEPLOYMENT")  
  
# Initialize the Azure OpenAI client  
client = AzureOpenAI(  
    azure_endpoint=aoai_endpoint,  
    api_key=aoai_api_key,  
    api_version="2024-10-21"  
)  
  
def image_to_data_url(image_bytes, mime_type='image/png'):  
    """  
    Convert image bytes to a data URL.  
  
    Parameters:  
    -----------  
    image_bytes : bytes  
        The image data in bytes.  
    mime_type : str  
        The MIME type of the image.  
  
    Returns:  
    --------  
    str  
        A data URL representing the image.  
    """  
    base64_encoded_data = base64.b64encode(image_bytes).decode('utf-8')  
    return f"data:{mime_type};base64,{base64_encoded_data}"  
  
def call_azure_openai(prompt, image_data_url, response_format, client=client, aoai_deployment_name=aoai_deployment_name):  
    """  
    Call the Azure OpenAI service to analyze an image.  
  
    Parameters:  
    -----------  
    prompt : str  
        The prompt to send to the model.  
    image_data_url : str  
        The data URL of the image.  
    response_format : BaseModel  
        The pydantic BaseModel defining the expected structured output.  
    client : AzureOpenAI  
        The Azure OpenAI client instance.  
    aoai_deployment_name : str  
        The deployment name of the Azure OpenAI model.  
  
    Returns:  
    --------  
    dict  
        The parsed response from the Azure OpenAI model.  
    """  
  
    completion = client.beta.chat.completions.parse(  
        model=aoai_deployment_name,  
        messages=[{  
            "role": "system",  
            "content": "You are an expert assistant that extracts information from documents."  
        }, {  
            "role": "user",  
            "content": [{  
                "type": "text",  
                "text": prompt  
            }, {  
                "type": "image_url",  
                "image_url": {  
                    "url": image_data_url  
                }  
            }]  
        }],  
        max_tokens=4096,  
        temperature=0.4,  
        response_format=response_format  
    )  
  
    response = json.loads(completion.model_dump_json(indent=2))  
  
    extracted_information = response['choices'][0]['message']['parsed']  
  
    return extracted_information  
  
def main():  
    # Define input and output directories  
    input_dir = Path('input_documents')  
    output_dir = Path('output_results')  
    output_dir.mkdir(exist_ok=True)  
  
    # Define output images directory  
    output_images_dir = Path('output_images')  
    output_images_dir.mkdir(exist_ok=True)  
  
    # Prompt to extract specific information  
    prompt = """ From the given document, extract:
    1) The page number. It will be at the bottom of the page.
    2) The Requirement ID and requirement text for each requirement. 
        The requirement ID will be in the left side of the page, and it will be in the format of a number followed by a dot followed by numbers. For example: 2.3 or 3.7.9
        The requirement text will be on the center to right side of the page, and it will be one or more paragraphs of text. If you see a list, such as (a), (b), (c), etc., please include that as part of the requirement text.
        If, at the beggining of the page, you see requirement text paragraphs with no requirement ID next to them, for requirement ID write "See previous ID" and for requirement text write the text of the requirement.
        If the requirement text includes a table, write the table in markdown format."""  
  
    # Define the structured output format using pydantic
    class Requirement(BaseModel):
        RequirementID: str
        RequirementText: str

    class ExtractedInformation(BaseModel):  
        pageNumber: int
        extractedText: list[Requirement]  
  
    # Iterate over each PDF in the input directory  
    for pdf_file in input_dir.glob('*.pdf'):  
        if pdf_file.is_file():  
            print(f"Processing {pdf_file.name}...")  
  
            # Open the PDF file  
            try:  
                doc = fitz.open(pdf_file)  
            except Exception as e:  
                print(f"Error opening {pdf_file.name}: {e}")  
                continue  
  
            # Iterate over each page in the PDF  
            for page_number in range(len(doc)):  
                try:  
                    # Load the page  
                    page = doc.load_page(page_number)  
                    zoom = 2  # Zoom factor for image quality  
                    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))  
                    image_bytes = pix.tobytes()  
  
                    # Save the image to output_images directory  
                    image_output_path = output_images_dir / f"{pdf_file.stem}_page{page_number+1}.png"  
                    pix.save(str(image_output_path))  
                    print(f"Saved image to {image_output_path.name}")  
  
                    # Print the image size and dimensions  
                    image_size = os.path.getsize(str(image_output_path))  
                    print(f"Image size: {image_size} bytes")  
                    print(f"Image dimensions: {pix.width}x{pix.height}")  

                    # Convert image to data URL  
                    image_data_url = image_to_data_url(image_bytes) 

                    # Call Azure OpenAI to extract structured information  
                    extracted_info = call_azure_openai(prompt, image_data_url, response_format=ExtractedInformation)  
   
                    # Define output file path  
                    output_file = output_dir / f"{pdf_file.stem}_page{page_number+1}.json" 

                    # Save the result as a JSON file  
                    with open(output_file, 'w', encoding='utf-8') as json_file:  
                        json.dump(extracted_info, json_file, ensure_ascii=False, indent=2) 

                    print(f"Saved extracted information to {output_file.name}")    
  
                except Exception as e:  
                    print(f"Error processing page {page_number+1} of {pdf_file.name}: {e}")  
  
if __name__ == "__main__":  
    main()  