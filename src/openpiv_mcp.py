from mcp.server.fastmcp import FastMCP
from openpiv import tools, pyprocess
import numpy as np
import pandas as pd
import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for PNG generation
import matplotlib.pyplot as plt

# Initialize the FastMCP server
mcp = FastMCP("OpenPIV-Server")

@mcp.tool()
def compute_piv(
    image_a_path: str, 
    image_b_path: str, 
    window_size: int = 32, 
    overlap: int = 16, 
    dt: float = 1.0,
    output_dir: str = ""
) -> str:
    """
    Computes Particle Image Velocimetry (PIV) on two images.
    Use this tool when the user asks to analyze flow, movement, or PIV on two frames.
    
    Args:
        image_a_path: Absolute path to the first image frame.
        image_b_path: Absolute path to the second image frame.
        window_size: Interrogation window size (default 32).
        overlap: Overlap between windows (default 16).
        dt: Time delay between frames (default 1.0).
        output_dir: Where to save the CSV. Defaults to a temp directory.
    """
    if not os.path.exists(image_a_path) or not os.path.exists(image_b_path):
        return "Error: Image paths provided do not exist."

    try:
        # 1. Read Images
        frame_a = tools.imread(image_a_path)
        frame_b = tools.imread(image_b_path)

        frame_a = frame_a.astype(np.int32)
        frame_b = frame_b.astype(np.int32)

        # 2. Process PIV
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

        # 3. Structure Output Data
        # Flatten arrays to create a table of x, y, u, v, s2n
        df = pd.DataFrame({
            'x': x.flatten(),
            'y': y.flatten(),
            'u': u.flatten(),
            'v': v.flatten(),
            's2n': s2n.flatten()
        })
        
        # 4. Save to CSV
        if not output_dir:
            output_dir = tempfile.gettempdir()
        
        output_path = os.path.join(output_dir, "piv_results.csv")
        df.to_csv(output_path, index=False)

        # 5. Calculate summary statistics for the LLM
        valid_vectors = df[df['s2n'] > 1.0] # Simple threshold example
        max_u = df['u'].max()
        max_v = df['v'].max()
        mean_u = df['u'].mean()

        # 6. Return response to the LLM
        return (
            f"PIV computation successful!\n"
            f"Full data saved to: {output_path}\n"
            f"Summary Statistics:\n"
            f"- Total vectors computed: {len(df)}\n"
            f"- Mean U velocity: {mean_u:.4f}\n"
            f"- Max U velocity: {max_u:.4f}\n"
            f"- Max V velocity: {max_v:.4f}\n"
            f"The LLM can now use pandas or python tools to plot the data from {output_path} if requested."
        )

    except Exception as e:
        return f"An error occurred during OpenPIV computation: {str(e)}"


@mcp.tool()
def create_quiver_plot(
    csv_path: str,
    output_path: str = "",
    title: str = "PIV Velocity Field",
    scale: int = 50,
    width: float = 0.003,
    cmap: str = "viridis"
) -> str:
    """
    Creates a quiver (vector field) plot from PIV results CSV.
    Use this tool when the user wants to visualize the flow field.

    Args:
        csv_path: Path to the PIV results CSV file.
        output_path: Where to save the PNG. Defaults to CSV directory.
        title: Plot title (default "PIV Velocity Field").
        scale: Quiver scale factor (default 50, higher = shorter arrows).
        width: Arrow width (default 0.003).
        cmap: Colormap for velocity magnitude (default "viridis").
    """
    if not os.path.exists(csv_path):
        return "Error: CSV file does not exist."

    try:
        # Read CSV data
        df = pd.read_csv(csv_path)
        
        # Reshape to 2D grids
        x = df['x'].values
        y = df['y'].values
        u = df['u'].values
        v = df['v'].values
        
        # Get unique coordinates to determine grid shape
        x_unique = np.unique(x)
        y_unique = np.unique(y)
        nx, ny = len(x_unique), len(y_unique)
        
        # Reshape to 2D
        X = x.reshape(ny, nx)
        Y = y.reshape(ny, nx)
        U = u.reshape(ny, nx)
        V = v.reshape(ny, nx)
        
        # Calculate velocity magnitude for coloring
        magnitude = np.sqrt(U**2 + V**2)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create quiver plot with colored arrows
        q = ax.quiver(X, Y, U, V, magnitude, cmap=cmap, 
                      scale=scale, width=width, alpha=0.8)
        
        # Add colorbar
        cbar = plt.colorbar(q, ax=ax, label='Velocity Magnitude (pixels/dt)')
        
        # Set labels and title
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.set_title(title)
        ax.set_aspect('equal')
        
        # Determine output path
        if not output_path:
            output_path = os.path.join(os.path.dirname(csv_path), "piv_quiver.png")
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return (
            f"Quiver plot created successfully!\n"
            f"Saved to: {output_path}\n"
            f"Plot details:\n"
            f"- Grid size: {nx} x {ny} vectors\n"
            f"- Velocity range: {magnitude.min():.4f} to {magnitude.max():.4f}\n"
            f"- Colormap: {cmap}"
        )
        
    except Exception as e:
        return f"An error occurred while creating the quiver plot: {str(e)}"


if __name__ == "__main__":
    # Runs the server over stdio (standard for local MCP clients like Claude Desktop)
    mcp.run()