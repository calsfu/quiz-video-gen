from dataclasses import dataclass

from moviepy import ColorClip
import numpy as np

from moviepy.Clip import Clip
from moviepy.Effect import Effect

# Helper function to create a radial gradient
def create_radial_gradient(w, h, center_color, edge_color, radius_factor=0.7):
    """
    Creates a numpy array for a radial gradient image.
    
    Args:
        w (int): Width of the image.
        h (int): Height of the image.
        center_color (list or tuple): RGB color at the center.
        edge_color (list or tuple): RGB color at the edges.
        radius_factor (float): Controls how far the gradient extends. 
                               1.0 means it touches the edges.
    
    Returns:
        numpy.ndarray: A (h, w, 3) numpy array representing the image.
    """
    y, x = np.ogrid[:h, :w]
    center_x, center_y = w / 2, h / 2
    
    # Calculate the distance of each pixel from the center
    # The radius is based on the smaller of the width or height to keep it circular
    radius = min(w, h) * radius_factor
    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    # Normalize the distance to a 0-1 scale, clipping values outside the radius
    mask = np.clip(dist / radius, 0, 1)
    
    # Create the gradient by interpolating between the center and edge colors
    # The 'mask[..., np.newaxis]' part is needed to correctly broadcast the arrays
    gradient = np.array(center_color) * (1 - mask[..., np.newaxis]) + \
               np.array(edge_color) * mask[..., np.newaxis]
               
    return gradient.astype('uint8')

@dataclass
class RadialGradientBlend(Effect):
    """
    Multiplies the clip's colors by the given factor, can be used
    to decrease or increase the clip's brightness (is that the
    right word ?)
    """
    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip pixel by pixel."""

        def process_frame(frame: np.ndarray) -> np.ndarray:
            # # Create a new array to hold the result.
            # # Using a float type during calculation avoids data-type issues.
            # processed_frame = np.zeros(frame.shape, dtype=np.float64)

            # # Iterate over each pixel using its coordinates (y, x)
            # for y in range(frame.shape[0]):  # Iterate through rows (height)
            #     for x in range(frame.shape[1]):  # Iterate through columns (width)
            #         # Get the original pixel [R, G, B] and apply the factor
            #         new_pixel = self.factor * frame[y, x]
                    
            #         # Clamp the values to a max of 255
            #         processed_frame[y, x] = np.minimum(255, new_pixel)
            
            # # Convert the final frame to the standard 8-bit integer format
            # return processed_frame.astype("uint8")
            frame = frame + create_radial_gradient(
                frame.shape[1], 
                frame.shape[0],
                center_color=(25, 25, 25),  # Brighter at the center
                edge_color=(0, 0, 0),       # Empty at the edges
            )
            return np.clip(frame, 0, 255).astype("uint8")

        return clip.image_transform(process_frame)

def main():
    background_clip = ColorClip(size=(640, 320), color=(85, 183, 63), duration=1)
    radial_gradient = RadialGradientBlend(factor=1.5)
    blended_clip = radial_gradient.apply(background_clip)
    
    # Save or display the blended clip as needed
    blended_clip.write_videofile("radial_gradient_output.mp4", fps=24)

if __name__ == "__main__":
    main()
    