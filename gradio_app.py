#!/usr/bin/env python3
"""
OpenPIV MCP Server with Gradio for Hugging Face Spaces.

Gradio automatically exposes MCP endpoints at /gradio_api/mcp/
"""

import gradio as gr
from openpiv import tools, pyprocess
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile
import os
from PIL import Image
import requests
from io import BytesIO


def _load_image(image_input):
    """Load image from URL or base64 data."""
    if isinstance(image_input, Image.Image):
        return image_input
    elif isinstance(image_input, str):
        if image_input.startswith('http://') or image_input.startswith('https://'):
            response = requests.get(image_input)
            return Image.open(BytesIO(response.content))
        elif image_input.startswith('data:image'):
            # Handle base64 data URLs: data:image/png;base64,xxxx
            import base64
            data = image_input.split(',')[1]
            return Image.open(BytesIO(base64.b64decode(data)))
        else:
            # Try as file path (for local testing)
            import os
            if os.path.exists(image_input):
                return Image.open(image_input)
            raise ValueError(f"Invalid image format. Provide URL or base64 data URL. Received: {image_input[:100]}")
    else:
        raise ValueError(f"Unsupported image type: {type(image_input)}")


def compute_piv(
    image_a,
    image_b,
    window_size: int = 32,
    overlap: int = 16,
    dt: float = 1.0
) -> str:
    """
    Compute Particle Image Velocimetry (PIV) velocity field from two images.
    
    Args:
        image_a: First image frame (file path, URL, or PIL Image)
        image_b: Second image frame (file path, URL, or PIL Image)
        window_size: Interrogation window size in pixels (default 32)
        overlap: Overlap between adjacent windows in pixels (default 16)
        dt: Time delay between frames in seconds (default 1.0)
    
    Returns:
        Summary statistics and path to CSV file with velocity data
    """
    try:
        # Load images
        frame_a = np.array(_load_image(image_a)).astype(np.int32)
        frame_b = np.array(_load_image(image_b)).astype(np.int32)
        
        # Handle RGB images by converting to grayscale
        if len(frame_a.shape) == 3:
            frame_a = np.mean(frame_a, axis=2)
        if len(frame_b.shape) == 3:
            frame_b = np.mean(frame_b, axis=2)
        
        # Process PIV
        u, v, s2n = pyprocess.extended_search_area_piv(
            frame_a, frame_b,
            window_size=window_size,
            overlap=overlap,
            dt=dt,
            search_area_size=window_size
        )
        x, y = pyprocess.get_coordinates(
            image_size=frame_a.shape,
            search_area_size=window_size,
            overlap=overlap
        )
        
        # Create DataFrame
        df = pd.DataFrame({
            'x': x.flatten(),
            'y': y.flatten(),
            'u': u.flatten(),
            'v': v.flatten(),
            's2n': s2n.flatten()
        })
        
        # Save to CSV
        output_path = os.path.join(tempfile.gettempdir(), "piv_results.csv")
        df.to_csv(output_path, index=False)
        
        # Summary statistics
        valid_vectors = df[df['s2n'] > 1.0]
        return (
            f"**PIV computation successful!**\n\n"
            f"**Summary Statistics:**\n"
            f"- Total vectors computed: {len(df)}\n"
            f"- Valid vectors (s2n>1): {len(valid_vectors)}\n"
            f"- Mean U velocity: {df['u'].mean():.4f}\n"
            f"- Max U velocity: {df['u'].max():.4f}\n"
            f"- Max V velocity: {df['v'].max():.4f}\n\n"
            f"Full data saved to: `{output_path}`"
        )
    except Exception as e:
        import traceback
        return f"**Error:** {str(e)}\n\n{traceback.format_exc()}"


def create_quiver_plot(
    csv_file,
    title: str = "PIV Velocity Field",
    scale: int = 50,
    cmap: str = "viridis"
) -> Image.Image:
    """
    Create a quiver (vector field) plot from PIV results CSV.
    
    Args:
        csv_file: Path to or file object containing PIV results CSV
        title: Plot title (default "PIV Velocity Field")
        scale: Quiver scale factor - higher values = shorter arrows (default 50)
        cmap: Colormap for velocity magnitude (default "viridis")
    
    Returns:
        PIL Image of the quiver plot
    """
    try:
        # Handle file upload vs path
        if hasattr(csv_file, 'name'):
            csv_path = csv_file.name
        elif isinstance(csv_file, str):
            csv_path = csv_file
        else:
            raise ValueError(f"Unsupported CSV file type: {type(csv_file)}")
        
        df = pd.read_csv(csv_path)
        
        # Reshape to 2D grids
        x_unique = np.unique(df['x'].values)
        y_unique = np.unique(df['y'].values)
        nx, ny = len(x_unique), len(y_unique)
        
        X = df['x'].values.reshape(ny, nx)
        Y = df['y'].values.reshape(ny, nx)
        U = df['u'].values.reshape(ny, nx)
        V = df['v'].values.reshape(ny, nx)
        
        magnitude = np.sqrt(U**2 + V**2)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))
        q = ax.quiver(X, Y, U, V, magnitude, cmap=cmap, 
                      scale=scale, width=0.003, alpha=0.8)
        plt.colorbar(q, ax=ax, label='Velocity Magnitude (pixels/dt)')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.set_title(title)
        ax.set_aspect('equal')
        
        # Save to temp file and load as PIL
        output_path = os.path.join(tempfile.gettempdir(), "piv_quiver.png")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return Image.open(output_path)
    except Exception as e:
        import traceback
        raise gr.Error(f"Error creating plot: {str(e)}\n{traceback.format_exc()}")


# Create Gradio interface
with gr.Blocks(title="OpenPIV MCP Server") as demo:
    gr.Markdown("# 🌊 OpenPIV MCP Server")
    gr.Markdown("Particle Image Velocimetry (PIV) analysis for fluid dynamics research")
    
    with gr.Tab("📊 PIV Analysis"):
        gr.Markdown("Upload two consecutive frames to compute the velocity field")
        
        with gr.Row():
            img_a = gr.Image(label="Frame A (First Image)", type="pil")
            img_b = gr.Image(label="Frame B (Second Image)", type="pil")
        
        with gr.Row():
            window_size = gr.Number(label="Window Size", value=32, minimum=8, maximum=128)
            overlap = gr.Number(label="Overlap", value=16, minimum=4, maximum=64)
            dt = gr.Number(label="Time Delay (dt)", value=1.0, step=0.1)
        
        piv_btn = gr.Button("🔬 Compute PIV", variant="primary")
        piv_output = gr.Markdown(label="Results")
        
        piv_btn.click(
            fn=compute_piv,
            inputs=[img_a, img_b, window_size, overlap, dt],
            outputs=piv_output
        )
    
    with gr.Tab("🗺️ Quiver Plot"):
        gr.Markdown("Upload a PIV results CSV to create a vector field visualization")
        
        csv_file = gr.File(label="PIV Results CSV")
        
        with gr.Row():
            plot_title = gr.Textbox(label="Plot Title", value="PIV Velocity Field")
            scale = gr.Slider(label="Arrow Scale", minimum=10, maximum=200, value=50)
        
        plot_btn = gr.Button("📈 Create Quiver Plot", variant="primary")
        plot_output = gr.Image(label="Velocity Field Visualization")
        
        plot_btn.click(
            fn=create_quiver_plot,
            inputs=[csv_file, plot_title, scale],
            outputs=plot_output
        )
    
    gr.Markdown("""
    ---
    **MCP Endpoint:** `/gradio_api/mcp/`
    
    **Usage with MCP clients:**
    - Claude Desktop, Cursor, Windsurf can connect to this server
    - URL: `https://your-space.hf.space/gradio_api/mcp/`
    """)

# Launch with MCP server enabled
if __name__ == "__main__":
    import os
    
    # Get port from environment (Hugging Face Spaces)
    port = int(os.environ.get("PORT", 7860))
    
    # Launch with MCP server enabled and verbose errors
    demo.launch(
        server_port=port,
        server_name="0.0.0.0",
        mcp_server=True,  # Enable MCP!
        show_error=True,  # Show detailed errors
    )
