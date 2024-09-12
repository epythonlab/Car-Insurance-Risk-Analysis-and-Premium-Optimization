import os
import zipfile
import pandas as pd
import io

def extract_zip(zip_file_path: str, extract_to: str) -> None:
    """
    Extracts a zip file to the specified directory.

    Args:
        zip_file_path (str): The path to the zip file.
        extract_to (str): The directory where the zip contents will be extracted.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def extract_nested_zip(outer_zip_path: str, extract_to: str) -> None:
    """
    Extracts a zip file and any nested zip files within it.

    Args:
        outer_zip_path (str): Path to the outer zip file.
        extract_to (str): Directory where the contents will be extracted.
    """
    with zipfile.ZipFile(outer_zip_path, 'r') as outer_zip:
        for file_info in outer_zip.infolist():
            if file_info.filename.endswith(".zip"):
                # Handle the nested zip
                with outer_zip.open(file_info.filename) as nested_zip_file:
                    nested_zip_data = io.BytesIO(nested_zip_file.read())
                    with zipfile.ZipFile(nested_zip_data, 'r') as nested_zip:
                        nested_zip.extractall(extract_to)
            else:
                # Extract regular files
                outer_zip.extract(file_info, extract_to)

def load_txt_from_zip(extracted_dir: str, filename: str) -> pd.DataFrame:
    """
    Loads a pipe-separated TXT file from the extracted directory into a pandas DataFrame.

    Args:
        extracted_dir (str): The directory where the zip contents were extracted.
        filename (str): The name of the TXT file to load.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    file_path = os.path.join(extracted_dir, filename)
    
    # Load the .txt file as pipe-separated (|)
    df = pd.read_csv(file_path, delimiter='|', low_memory=False)
    return df

def load_data(outer_zip_path: str, filename: str) -> pd.DataFrame:
    """
    Orchestrates the extraction and loading of data from a nested zip file.

    Args:
        outer_zip_path (str): Path to the outer zip file.
        filename (str): The name of the TXT file to load.

    Returns:
        pd.DataFrame: The processed data as a pandas DataFrame.
    """
    try:
        # Create a directory for extracted files
        extract_to = "../data/"
        os.makedirs(extract_to, exist_ok=True)
        
        # Extract the nested zip file and any files within
        extract_nested_zip(outer_zip_path, extract_to)
        
        # Load the TXT file from the extracted directory
        df = load_txt_from_zip(extract_to, filename)

        return df
    
    except Exception as e:
        raise RuntimeError(f'Error loading data: {str(e)}')