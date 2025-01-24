# Anchor Text Cannibalization Analyzer

A Streamlit web application that helps identify SEO issues related to anchor text cannibalization in your website's internal linking structure.

## What is Anchor Text Cannibalization?

Anchor text cannibalization occurs when the same anchor text is used to link to different URLs across your website. This can confuse search engines about which page is most relevant for that particular keyword/phrase, potentially affecting your SEO performance.

## Features

- Upload and analyze CSV/Excel files containing internal linking data
- Smart filtering of URLs to focus on SEO-valuable content:
  - Excludes URLs with parameters (#, ?, =)
  - Filters out pagination URLs (/page/1/, etc.)
  - Removes user-related pages (login, signup, etc.)
  - Excludes non-SEO content (authors, webinars, news, etc.)
- Detailed analysis of anchor text usage:
  - Total occurrences of each anchor text
  - Number of different destinations per anchor text
  - Percentage distribution of destinations
  - Source pages for each anchor text
- Visual representation through dual charts:
  - Total occurrences visualization
  - Unique destinations comparison
- Interactive visualization of problematic anchor texts
- Detailed breakdown of each cannibalization case
- User-friendly interface with expandable sections

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

2. Upload your file through the web interface
   - Your file must contain these columns:
     - `Source`: The page where the link is located
     - `Destination`: The page being linked to
     - `Anchor`: The anchor text used for the link
   - Supported file formats:
     - CSV files (.csv)
     - Excel files (.xlsx, .xls)

3. View the analysis results:
   - Total number of cannibalization cases
   - Detailed breakdown for each anchor text
   - Visual representation of the data

## Analysis Results

The tool provides two main views:

1. **Detailed Analysis Tab**
   - Complete statistics for each anchor text
   - Total occurrences and unique destinations
   - Percentage breakdown of URL usage
   - List of source pages using each anchor text

2. **Visualization Tab**
   - Total Occurrences Chart: Shows how many times each anchor text appears
   - Different Destinations Chart: Shows how many unique URLs each anchor text points to

## File Format

Your file should follow this structure (shown as a table):

| Source | Destination | Anchor |
|--------|-------------|--------|
| https://example.com/page1 | https://example.com/target1 | Example Anchor Text |
| https://example.com/page2 | https://example.com/target2 | Example Anchor Text |

## Requirements

- Python 3.7+
- Streamlit 1.29.0
- Pandas 2.1.4
- Plotly 5.18.0
- OpenPyXL 3.1.2

## License

This project is open source and available under the MIT License.
