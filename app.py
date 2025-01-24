import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re
import json
from io import BytesIO
import base64
from datetime import datetime

def is_non_seo_url(url):
    """Check if URL should be excluded from SEO analysis."""
    # Convert to lowercase for case-insensitive matching
    url_lower = url.lower()
    
    # Special parameters check
    if any(char in url for char in ['#', '?', '=']):
        return True
    
    # Pagination patterns
    if re.search(r'/page/\d+/?', url_lower):
        return True
    
    # User-related pages
    user_related_patterns = [
        '/login', '/signin', '/signup', '/register',
        '/dashboard', '/account', '/profile',
        '/terms', '/privacy', '/tos', '/terms-of-service',
        '/forgot-password', '/reset-password',
        '/my-', '/user/', '/users/',
        '/cookie-policy', '/legal'
    ]
    
    # Content types to exclude
    content_type_patterns = [
        '/author/', '/authors/',
        '/webinar', '/webinars',
        '/news/', '/press/',
        '/use-case', '/use-cases',
        '/case-study', '/case-studies',
        '/events/', '/event/',
        '/blog/author/', '/blog/tag/',
        '/category/', '/tag/',
        '/feed/', '/rss/',
        '/archive/', '/archives/'
    ]
    
    # Check if URL matches any exclusion pattern
    exclude_patterns = user_related_patterns + content_type_patterns
    return any(pattern in url_lower for pattern in exclude_patterns)

def get_csv_download_link(df, filename):
    """Generate a download link for a DataFrame as CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def export_detailed_analysis(exact_match_anchors, anchors, filtered_df):
    """Create a detailed analysis export DataFrame"""
    rows = []
    for anchor in exact_match_anchors:
        total_occurrences = len(anchors[anchor])
        unique_destinations = len(exact_match_anchors[anchor])
        
        # Get all destinations and their counts
        for target_url in exact_match_anchors[anchor]:
            url_count = anchors[anchor].count(target_url)
            percentage = (url_count / total_occurrences) * 100
            
            # Get source pages for this anchor and destination
            sources = filtered_df[
                (filtered_df['Anchor'] == anchor) & 
                (filtered_df['Destination'] == target_url)
            ]['Source'].unique()
            
            rows.append({
                'Anchor Text': anchor,
                'Total Occurrences': total_occurrences,
                'Unique Destinations': unique_destinations,
                'Destination URL': target_url,
                'Times Used': url_count,
                'Usage Percentage': f"{percentage:.1f}%",
                'Source Pages': '; '.join(sources)
            })
    
    return pd.DataFrame(rows)

st.set_page_config(page_title="Anchor Text Cannibalization Analyzer", layout="wide")

st.title("Anchor Text Cannibalization Analyzer")
st.markdown("""
This tool analyzes your internal linking structure to identify potential SEO issues 
where the same anchor text points to different URLs (anchor text cannibalization).
""")

# File uploader
uploaded_file = st.file_uploader("Upload your file", type=['csv', 'xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Read the file based on its type
        file_type = uploaded_file.name.split('.')[-1]
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        else:  # Excel file
            df = pd.read_excel(uploaded_file)
        
        # Initial row count
        total_rows = len(df)
        
        # Apply basic filters
        filtered_df = df[
            (df['Type'] == 'Hyperlink') &  # Only Hyperlinks
            (df['Anchor'].notna()) &       # Non-empty Anchor text
            (df['Status Code'] == 200) &   # Status code 200
            (df['Link Position'] == 'Content')  # Link Position is Content
        ].copy()
        
        # Filter out non-SEO URLs
        filtered_df = filtered_df[
            ~filtered_df['Source'].apply(is_non_seo_url) &
            ~filtered_df['Destination'].apply(is_non_seo_url)
        ]
        
        # Show filtering results
        st.info(f"""
        Filtering results:
        - Original rows: {total_rows}
        - After basic filters: {len(df[df['Type'] == 'Hyperlink'])}
        - Final rows (SEO-valuable content only): {len(filtered_df)}
        """)
        
        # Create a dictionary of anchor text and the pages it links to
        anchors = {}
        for _, row in filtered_df.iterrows():
            if row['Anchor'] in anchors:
                anchors[row['Anchor']].append(row['Destination'])
            else:
                anchors[row['Anchor']] = [row['Destination']]

        # Find the exact match anchors that are linking to more than one page
        exact_match_anchors = {}
        for anchor in anchors:
            target_urls = anchors[anchor]
            unique_target_urls = list(set(target_urls))
            if len(unique_target_urls) > 1:
                exact_match_anchors[anchor] = unique_target_urls

        # Display results
        if exact_match_anchors:
            st.warning(f"Found {len(exact_match_anchors)} cases of anchor text cannibalization in SEO-valuable content")
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["Detailed Analysis", "Visualization"])
            
            with tab1:
                # Create export DataFrame
                export_df = export_detailed_analysis(exact_match_anchors, anchors, filtered_df)
                
                # Add export button
                st.markdown("### Export Options")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.markdown(
                    get_csv_download_link(export_df, f"anchor_text_analysis_{timestamp}.csv"),
                    unsafe_allow_html=True
                )
                
                # Display detailed analysis
                for anchor in exact_match_anchors:
                    total_occurrences = len(anchors[anchor])
                    unique_destinations = len(exact_match_anchors[anchor])
                    with st.expander(f"Anchor Text: {anchor}"):
                        st.markdown(f"""
                        **Statistics:**
                        - Total occurrences: {total_occurrences}
                        - Number of different destinations: {unique_destinations}
                        """)
                        
                        st.markdown("\n**Links to these destinations:**")
                        for target_url in exact_match_anchors[anchor]:
                            url_count = anchors[anchor].count(target_url)
                            percentage = (url_count / total_occurrences) * 100
                            st.markdown(f"- {target_url} (used {url_count} times - {percentage:.1f}% of occurrences)")
                        
                        st.markdown("\n**Source pages using this anchor text:**")
                        sources = filtered_df[filtered_df['Anchor'] == anchor]['Source'].unique()
                        for source in sources:
                            st.markdown(f"- {source}")
            
            with tab2:
                st.markdown("### Export Options")
                st.markdown("*Note: You can download each chart as PNG by using the camera icon in the chart's toolbar*")
                
                # Create two bar charts: one for total occurrences and one for unique destinations
                tab2_col1, tab2_col2 = st.columns(2)
                
                with tab2_col1:
                    # Chart for total occurrences
                    total_occurrences = {anchor: len(anchors[anchor]) for anchor in exact_match_anchors}
                    fig1 = go.Figure(data=[
                        go.Bar(
                            x=list(total_occurrences.keys()),
                            y=list(total_occurrences.values()),
                            text=list(total_occurrences.values()),
                            textposition='auto',
                            name='Total Occurrences'
                        )
                    ])
                    fig1.update_layout(
                        title="Total Occurrences of Each Anchor Text",
                        xaxis_title="Anchor Text",
                        yaxis_title="Number of Total Uses",
                        height=500,
                        showlegend=True,
                        modebar_add=['downloadImage']
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with tab2_col2:
                    # Chart for unique destinations
                    unique_destinations = {anchor: len(urls) for anchor, urls in exact_match_anchors.items()}
                    fig2 = go.Figure(data=[
                        go.Bar(
                            x=list(unique_destinations.keys()),
                            y=list(unique_destinations.values()),
                            text=list(unique_destinations.values()),
                            textposition='auto',
                            name='Unique Destinations'
                        )
                    ])
                    fig2.update_layout(
                        title="Number of Different Destinations per Anchor Text",
                        xaxis_title="Anchor Text",
                        yaxis_title="Number of Different Destinations",
                        height=500,
                        showlegend=True,
                        modebar_add=['downloadImage']
                    )
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.success("No anchor text cannibalization found in SEO-valuable content!")

    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
        st.markdown("""
        Please make sure your file has the following columns:
        - **Type**: For filtering Hyperlinks
        - **Source**: The page where the link is located
        - **Destination**: The page being linked to
        - **Anchor**: The anchor text used for the link
        - **Status Code**: For filtering status 200
        - **Link Position**: For filtering Content links
        """)
