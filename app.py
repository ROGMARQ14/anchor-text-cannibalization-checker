import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
        
        # Apply filters
        filtered_df = df[
            (df['Type'] == 'Hyperlink') &  # Only Hyperlinks
            (df['Anchor'].notna()) &       # Non-empty Anchor text
            (df['Status Code'] == 200) &   # Status code 200
            (df['Link Position'] == 'Content')  # Link Position is Content
        ].copy()
        
        # Show filtering results
        st.info(f"Original rows: {len(df)} | Filtered rows: {len(filtered_df)}")
        
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
            st.warning(f"Found {len(exact_match_anchors)} cases of anchor text cannibalization")
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["Detailed Analysis", "Visualization"])
            
            with tab1:
                for anchor in exact_match_anchors:
                    with st.expander(f"Anchor Text: {anchor} ({len(anchors[anchor])} total occurrences)"):
                        st.markdown("**Links to these destinations:**")
                        for target_url in exact_match_anchors[anchor]:
                            url_count = anchors[anchor].count(target_url)
                            st.markdown(f"- {target_url} (used {url_count} times)")
                        
                        # Show source pages for this anchor text
                        st.markdown("\n**Source pages using this anchor text:**")
                        sources = filtered_df[filtered_df['Anchor'] == anchor]['Source'].unique()
                        for source in sources:
                            st.markdown(f"- {source}")
            
            with tab2:
                # Create a bar chart showing the most problematic anchor texts
                anchor_counts = {anchor: len(urls) for anchor, urls in exact_match_anchors.items()}
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(anchor_counts.keys()),
                        y=list(anchor_counts.values()),
                        text=list(anchor_counts.values()),
                        textposition='auto',
                    )
                ])
                fig.update_layout(
                    title="Number of Different Destinations per Anchor Text",
                    xaxis_title="Anchor Text",
                    yaxis_title="Number of Different Destinations",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No anchor text cannibalization found! ")

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
