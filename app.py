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
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Create a dictionary of anchor text and the pages it links to
        anchors = {}
        for i, row in df.iterrows():
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
            st.success("No anchor text cannibalization found! 🎉")

    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
        st.markdown("Please make sure your CSV file has the following columns: **Source**, **Destination**, and **Anchor**")
