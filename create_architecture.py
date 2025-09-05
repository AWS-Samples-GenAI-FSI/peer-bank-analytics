#!/usr/bin/env python3
"""
Create architecture diagram for Banking Peer Analytics POC
Uses matplotlib and custom AWS-style icons
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

def create_architecture_diagram():
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Colors (AWS style)
    aws_orange = '#FF9900'
    aws_blue = '#232F3E'
    light_blue = '#4B91F1'
    light_gray = '#F2F3F3'
    dark_gray = '#666666'
    
    # Title
    ax.text(8, 9.5, 'Banking Peer Analytics - Architecture Flow', 
            fontsize=20, fontweight='bold', ha='center', color=aws_blue)
    
    # User/Client section
    user_box = FancyBboxPatch((0.5, 7.5), 2.5, 1.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor=light_blue, edgecolor=aws_blue, linewidth=2)
    ax.add_patch(user_box)
    ax.text(1.75, 8.25, '👤 User', fontsize=12, fontweight='bold', ha='center', color='white')
    ax.text(1.75, 7.9, 'Streamlit UI', fontsize=10, ha='center', color='white')
    
    # Streamlit Application
    streamlit_box = FancyBboxPatch((4, 7.5), 3, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#FF6B6B', edgecolor=aws_blue, linewidth=2)
    ax.add_patch(streamlit_box)
    ax.text(5.5, 8.4, '🖥️ Streamlit App', fontsize=12, fontweight='bold', ha='center', color='white')
    ax.text(5.5, 8.1, '1_🏠_Home.py', fontsize=9, ha='center', color='white')
    ax.text(5.5, 7.8, 'pages/*.py', fontsize=9, ha='center', color='white')
    
    # FDIC APIs
    fdic_box = FancyBboxPatch((8.5, 7.5), 3, 1.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor='#4ECDC4', edgecolor=aws_blue, linewidth=2)
    ax.add_patch(fdic_box)
    ax.text(10, 8.4, '🏛️ FDIC APIs', fontsize=12, fontweight='bold', ha='center', color='white')
    ax.text(10, 8.1, 'Institutions API', fontsize=9, ha='center', color='white')
    ax.text(10, 7.8, 'Financials API', fontsize=9, ha='center', color='white')
    
    # Amazon Bedrock
    bedrock_box = FancyBboxPatch((12.5, 7.5), 3, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=aws_orange, edgecolor=aws_blue, linewidth=2)
    ax.add_patch(bedrock_box)
    ax.text(14, 8.4, '🤖 Amazon Bedrock', fontsize=12, fontweight='bold', ha='center', color='white')
    ax.text(14, 8.1, 'Claude AI', fontsize=9, ha='center', color='white')
    ax.text(14, 7.8, 'Analysis Engine', fontsize=9, ha='center', color='white')
    
    # Data Processing Layer
    processing_box = FancyBboxPatch((2, 5.5), 12, 1.2, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor=light_gray, edgecolor=dark_gray, linewidth=2)
    ax.add_patch(processing_box)
    ax.text(8, 6.3, '⚙️ Data Processing & Analysis Layer', fontsize=14, fontweight='bold', ha='center', color=aws_blue)
    ax.text(8, 5.9, 'Real-time FDIC data retrieval • Historical quarterly analysis • AI-powered insights generation', 
            fontsize=10, ha='center', color=dark_gray)
    
    # Banking Metrics
    metrics = ['ROA', 'ROE', 'NIM', 'Tier 1', 'LDR', 'CRE']
    for i, metric in enumerate(metrics):
        x_pos = 1.5 + i * 2.2
        metric_box = FancyBboxPatch((x_pos, 3.8), 1.8, 0.8, 
                                    boxstyle="round,pad=0.05", 
                                    facecolor='#95E1D3', edgecolor=aws_blue, linewidth=1)
        ax.add_patch(metric_box)
        ax.text(x_pos + 0.9, 4.2, metric, fontsize=10, fontweight='bold', ha='center', color=aws_blue)
    
    ax.text(8, 3.4, '📊 6 Key Banking Metrics', fontsize=12, fontweight='bold', ha='center', color=aws_blue)
    
    # Visualization Layer
    viz_box = FancyBboxPatch((2, 2.2), 12, 1, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#A8E6CF', edgecolor=aws_blue, linewidth=2)
    ax.add_patch(viz_box)
    ax.text(8, 2.9, '📈 Interactive Visualizations (Plotly)', fontsize=12, fontweight='bold', ha='center', color=aws_blue)
    ax.text(8, 2.5, 'Line Charts • Bar Charts • Heatmaps • Trend Analysis', fontsize=10, ha='center', color=dark_gray)
    
    # Output Layer
    output_box = FancyBboxPatch((2, 0.5), 12, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#FFD93D', edgecolor=aws_blue, linewidth=2)
    ax.add_patch(output_box)
    ax.text(8, 1.2, '📋 AI-Generated Insights & Reports', fontsize=12, fontweight='bold', ha='center', color=aws_blue)
    ax.text(8, 0.8, 'Peer Comparisons • Performance Analysis • Downloadable Data', fontsize=10, ha='center', color=dark_gray)
    
    # Arrows showing flow
    # User to Streamlit
    ax.annotate('', xy=(4, 8.25), xytext=(3, 8.25), 
                arrowprops=dict(arrowstyle='->', lw=2, color=aws_blue))
    
    # Streamlit to FDIC
    ax.annotate('', xy=(8.5, 8.25), xytext=(7, 8.25), 
                arrowprops=dict(arrowstyle='->', lw=2, color=aws_blue))
    
    # Streamlit to Bedrock
    ax.annotate('', xy=(12.5, 8.25), xytext=(7, 8.25), 
                arrowprops=dict(arrowstyle='->', lw=2, color=aws_blue))
    
    # To Processing Layer
    ax.annotate('', xy=(8, 6.7), xytext=(8, 7.5), 
                arrowprops=dict(arrowstyle='->', lw=2, color=aws_blue))
    
    # To Metrics
    ax.annotate('', xy=(8, 4.6), xytext=(8, 5.5), 
                arrowprops=dict(arrowstyle='->', lw=2, color=aws_blue))
    
    # To Visualization
    ax.annotate('', xy=(8, 3.2), xytext=(8, 3.8), 
                arrowprops=dict(arrowstyle='->', lw=2, color=aws_blue))
    
    # To Output
    ax.annotate('', xy=(8, 1.5), xytext=(8, 2.2), 
                arrowprops=dict(arrowstyle='->', lw=2, color=aws_blue))
    
    # Flow numbers
    flow_steps = [
        (1.75, 7.3, '1'),
        (5.5, 7.3, '2'),
        (10, 7.3, '3'),
        (14, 7.3, '4'),
        (8.5, 6.7, '5'),
        (8.5, 4.6, '6'),
        (8.5, 3.2, '7'),
        (8.5, 1.5, '8')
    ]
    
    for x, y, num in flow_steps:
        circle = plt.Circle((x, y), 0.15, color=aws_orange, zorder=10)
        ax.add_patch(circle)
        ax.text(x, y, num, fontsize=10, fontweight='bold', ha='center', va='center', color='white', zorder=11)
    
    # Banks list
    banks_text = "10 Major US Banks:\nJPMorgan Chase • Bank of America • Wells Fargo • Citibank • U.S. Bank\nPNC Bank • Goldman Sachs • Truist Bank • Capital One • TD Bank"
    ax.text(0.5, 0.2, banks_text, fontsize=9, ha='left', va='bottom', color=dark_gray,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor=dark_gray, alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('images/architecture.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print("✅ Architecture diagram created: images/architecture.png")

if __name__ == "__main__":
    create_architecture_diagram()