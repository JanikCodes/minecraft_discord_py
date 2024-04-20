def hex_to_rgb(hex_color):
    """Converts a hex color string to an RGB tuple."""
    # Remove the '#' character if present
    hex_color = hex_color.lstrip('#')
    # Convert hex color string to RGB tuple
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))