# Anchor Text Cannibalization Analyzer

A Streamlit web application that helps identify SEO issues related to anchor text cannibalization in your website's internal linking structure.

## What is Anchor Text Cannibalization?

Anchor text cannibalization occurs when the same anchor text is used to link to different URLs across your website. This can confuse search engines about which page is most relevant for that particular keyword/phrase, potentially affecting your SEO performance.

## Features

- Upload and analyze CSV files containing internal linking data
- Interactive visualization of problematic anchor texts
- Detailed breakdown of each cannibalization case
- User-friendly interface with expandable sections
- Visual representation of data through charts

## Installation

1. Clone this repository or download the files
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Upload your CSV file through the web interface
   - Your CSV file must contain these columns:
     - `Source`: The page where the link is located
     - `Destination`: The page being linked to
     - `Anchor`: The anchor text used for the link

3. View the analysis results:
   - Total number of cannibalization cases
   - Detailed breakdown for each anchor text
   - Visual representation of the data

## CSV File Format

Your CSV file should follow this structure:

```csv
Source,Destination,Anchor
https://example.com/page1,https://example.com/target1,Example Anchor Text
https://example.com/page2,https://example.com/target2,Example Anchor Text
```

## Requirements

- Python 3.7+
- Streamlit 1.29.0
- Pandas 2.1.4
- Plotly 5.18.0

## License

This project is open source and available under the MIT License.
