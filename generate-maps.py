import numpy as np
from PIL import Image
import json

# Load configuration
with open('liquid-glass-config.json', 'r') as f:
    config = json.load(f)

# Extract config values
SELECTOR_WIDTH = config['selector']['hoverWidth']
SELECTOR_HEIGHT = config['selector']['hoverHeight']
CORNER_RADIUS = config['selector']['cornerRadius']
MAP_WIDTH = config['maps']['width']
MAP_HEIGHT = config['maps']['height']
LENS_DIAMETER = config['magnification']['lensDiameter']
RADIUS_OF_CURVATURE_FACTOR = config['magnification']['radiusOfCurvatureFactor']
MAG_MAX_DISPLACEMENT = config['magnification']['maxDisplacement']
BEZEL_WIDTH_FRACTION = config['bezel']['widthFraction']
BEZEL_GLASS_THICKNESS = config['bezel']['glassThickness']
SPECULAR_ANGLE = config['specular']['angle']
SPECULAR_EDGE_WIDTH = config['specular']['edgeWidth']
SPECULAR_EDGE_FALLOFF_POWER = config['specular']['edgeFalloffPower']
SPECULAR_ANGULAR_SHARPNESS = config['specular']['angularSharpnessPower']

def surface_height_squircle(x):
    """Convex squircle surface function (Apple's preferred)
    x: 0 (edge) to 1 (flat interior)
    returns: height from 0 to 1
    """
    return np.power(1 - np.power(1 - x, 4), 0.25)

def calculate_displacement_at_distance(distance_from_edge, bezel_width, glass_thickness, refractive_index=1.5):
    """Calculate displacement for a ray at given distance from edge
    Using proper surface normal and Snell's law
    """
    if distance_from_edge > bezel_width:
        return 0  # Flat interior, no displacement
    
    # Normalize position in bezel (0 at edge, 1 at flat start)
    bezel_pos = distance_from_edge / bezel_width
    
    # Surface height at this position
    height = surface_height_squircle(bezel_pos) * glass_thickness
    
    # Calculate surface normal using derivative
    delta = 0.001
    h1 = surface_height_squircle(max(0, bezel_pos - delta)) * glass_thickness
    h2 = surface_height_squircle(min(1, bezel_pos + delta)) * glass_thickness
    derivative = (h2 - h1) / (2 * delta * bezel_width)
    
    # Normal vector (derivative rotated by -90°)
    normal_x = -derivative
    normal_y = 1.0
    normal_mag = np.sqrt(normal_x**2 + normal_y**2)
    normal_x /= normal_mag
    normal_y /= normal_mag
    
    # Incident ray (orthogonal to background)
    incident_x = 0
    incident_y = 1
    
    # Snell's law: n1 * sin(θ1) = n2 * sin(θ2)
    n1 = 1.0  # air
    n2 = refractive_index  # glass
    
    # Calculate angle of incidence (angle between incident ray and normal)
    cos_theta1 = incident_x * normal_x + incident_y * normal_y
    sin_theta1 = np.sqrt(1 - cos_theta1**2)
    
    # Calculate refracted angle
    sin_theta2 = (n1 / n2) * sin_theta1
    
    # Check for total internal reflection
    if abs(sin_theta2) > 1:
        return 0  # Total internal reflection, no displacement
    
    cos_theta2 = np.sqrt(1 - sin_theta2**2)
    
    # Refracted ray direction
    refracted_x = (n1/n2) * incident_x + ((n1/n2) * cos_theta1 - cos_theta2) * normal_x
    refracted_y = (n1/n2) * incident_y + ((n1/n2) * cos_theta1 - cos_theta2) * normal_y
    
    # Displacement is how far the ray travels through the glass
    # For simplicity, use the horizontal component of displacement
    displacement = refracted_x * glass_thickness / refracted_y if refracted_y != 0 else 0
    
    return displacement

def rounded_rect_sdf(x, y, width, height, radius):
    """Signed distance function for rounded rectangle (pill shape)
    Returns distance from edge: negative inside, positive outside, 0 at edge
    """
    center_x = width / 2
    center_y = height / 2
    
    # Distance from center
    dx = abs(x - center_x)
    dy = abs(y - center_y)
    
    # Rectangle with rounded corners
    rect_w = width / 2 - radius
    rect_h = height / 2 - radius
    
    # Distance to rounded rectangle edge
    qx = max(0, dx - rect_w)
    qy = max(0, dy - rect_h)
    dist_to_edge = np.sqrt(qx*qx + qy*qy) - radius
    
    return -dist_to_edge  # Negative inside, positive outside

def generate_magnification_map(width, height, corner_radius):
    """Generate magnification displacement map by cropping center of large circular lens
    This gives gentle center magnification like kube.io
    """
    # Generate a large circular lens with proper parabolic surface
    lens_diameter = LENS_DIAMETER
    full_lens = np.zeros((lens_diameter, lens_diameter, 4), dtype=np.uint8)
    
    lens_center_x = lens_diameter / 2
    lens_center_y = lens_diameter / 2
    max_radius = lens_diameter / 2
    
    # Radius of curvature for parabolic lens (larger = gentler lens)
    radius_of_curvature = lens_diameter * RADIUS_OF_CURVATURE_FACTOR
    max_displacement = MAG_MAX_DISPLACEMENT
    
    # Calculate displacements for full lens using parabolic surface
    for y in range(LENS_DIAMETER):
        for x in range(LENS_DIAMETER):
            dx = x - lens_center_x
            dy = y - lens_center_y
            r = np.sqrt(dx*dx + dy*dy)  # Distance from optical axis
            
            if r < max_radius:
                # Parabolic lens: slope = r / radius_of_curvature
                # This is smooth and continuous, zero at center
                slope = r / radius_of_curvature
                
                # Displacement magnitude increases linearly with radius
                displacement_mag = slope * max_displacement
                
                # Direction: radially outward from center
                if r > 0:
                    dir_x = dx / r
                    dir_y = dy / r
                    
                    # INWARD displacement (toward center = magnification)
                    displace_x = -dir_x * displacement_mag
                    displace_y = -dir_y * displacement_mag
                else:
                    # At exact center: zero displacement (no singularity!)
                    displace_x = 0
                    displace_y = 0
                
                # Normalize to 0-1 range for storage
                normalized_x = displace_x / max_displacement
                normalized_y = displace_y / max_displacement
                
                # Map to 0-255 (128 = neutral)
                full_lens[y, x, 0] = np.clip(128 + normalized_x * 127, 0, 255)
                full_lens[y, x, 1] = np.clip(128 + normalized_y * 127, 0, 255)
                full_lens[y, x, 2] = 130
                full_lens[y, x, 3] = 255
            else:
                full_lens[y, x] = [128, 128, 130, 255]
    
    # Crop the center region to match selector size
    crop_x_start = (LENS_DIAMETER - width) // 2
    crop_y_start = (LENS_DIAMETER - height) // 2
    
    cropped = full_lens[crop_y_start:crop_y_start+height, 
                        crop_x_start:crop_x_start+width]
    
    return Image.fromarray(cropped, 'RGBA'), max_displacement

def generate_displacement_map_proper(width, height, corner_radius, bezel_width_fraction):
    """Generate bezel refraction displacement map (edge distortion)"""
    img = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Glass properties
    max_bezel_px = min(width, height) / 2 * bezel_width_fraction
    glass_thickness = BEZEL_GLASS_THICKNESS
    
    max_displacement = 0
    displacements = {}
    
    # First pass: calculate all displacements
    for y in range(height):
        for x in range(width):
            sdf = rounded_rect_sdf(x, y, width, height, corner_radius)
            
            if sdf >= 0:  # Inside the shape
                distance_from_edge = sdf
                
                displacement_mag = calculate_displacement_at_distance(
                    distance_from_edge,
                    max_bezel_px,
                    glass_thickness
                )
                
                max_displacement = max(max_displacement, abs(displacement_mag))
                
                # Direction: perpendicular to nearest edge
                delta = 1
                sdf_right = rounded_rect_sdf(x + delta, y, width, height, corner_radius)
                sdf_up = rounded_rect_sdf(x, y - delta, width, height, corner_radius)
                
                grad_x = sdf_right - sdf
                grad_y = sdf - sdf_up
                
                grad_mag = np.sqrt(grad_x*grad_x + grad_y*grad_y) + 0.0001
                grad_x /= grad_mag
                grad_y /= grad_mag
                
                angle = np.arctan2(grad_y, grad_x)
                displacements[(x, y)] = (displacement_mag, angle)
    
    # Second pass: normalize and write to image
    for y in range(height):
        for x in range(width):
            if (x, y) in displacements:
                mag, angle = displacements[(x, y)]
                normalized_mag = mag / max_displacement if max_displacement > 0 else 0
                
                disp_x = np.cos(angle) * normalized_mag
                disp_y = np.sin(angle) * normalized_mag
                
                img[y, x, 0] = np.clip(128 + disp_x * 127, 0, 255)
                img[y, x, 1] = np.clip(128 + disp_y * 127, 0, 255)
                img[y, x, 2] = 130
                img[y, x, 3] = 255
            else:
                img[y, x] = [128, 128, 130, 255]
    
    return Image.fromarray(img, 'RGBA'), max_displacement

def generate_specular_map(width, height, corner_radius, angle_deg):
    """Generate beautiful specular highlight with smooth gradient
    Creates highlights at BOTH angle_deg and angle_deg+180 (opposite sides)
    More concentrated at edges with angular falloff
    angle_deg: light angle in degrees (0=right, 90=top, 180=left, 270=bottom)
    """
    img = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Convert angle to radians for both light directions
    angle_rad = np.deg2rad(angle_deg)
    light1_x = np.cos(angle_rad)
    light1_y = -np.sin(angle_rad)
    
    # Opposite side (180 degrees)
    angle_rad2 = np.deg2rad(angle_deg + 180)
    light2_x = np.cos(angle_rad2)
    light2_y = -np.sin(angle_rad2)
    
    for y in range(height):
        for x in range(width):
            sdf = rounded_rect_sdf(x, y, width, height, corner_radius)
            
            if sdf >= 0:  # Inside shape
                # Calculate surface normal (gradient of SDF)
                delta = 1
                sdf_right = rounded_rect_sdf(x + delta, y, width, height, corner_radius)
                sdf_up = rounded_rect_sdf(x, y - delta, width, height, corner_radius)
                
                grad_x = sdf_right - sdf
                grad_y = sdf - sdf_up
                grad_mag = np.sqrt(grad_x*grad_x + grad_y*grad_y) + 0.0001
                grad_x /= grad_mag
                grad_y /= grad_mag
                
                # Dot product with BOTH light directions
                alignment1 = grad_x * light1_x + grad_y * light1_y
                alignment1 = max(0, alignment1)
                
                alignment2 = grad_x * light2_x + grad_y * light2_y
                alignment2 = max(0, alignment2)
                
                # Use the maximum alignment from either light
                alignment = max(alignment1, alignment2)
                
                # Add angular sharpening for more angular concentration
                alignment = np.power(alignment, SPECULAR_ANGULAR_SHARPNESS)
                
                # Distance from edge for VERY SHARP gradient (highly concentrated at edges)
                edge_width = SPECULAR_EDGE_WIDTH
                
                if sdf < edge_width:
                    # Very sharp gradient from edge to interior
                    edge_factor = 1.0 - (sdf / edge_width)
                    edge_factor = np.power(edge_factor, SPECULAR_EDGE_FALLOFF_POWER)
                    
                    # Combine alignment and edge distance
                    intensity = alignment * edge_factor
                    
                    # Extra smoothstep for silky smooth transition
                    intensity = intensity * intensity * (3.0 - 2.0 * intensity)
                    
                    brightness = int(255 * intensity * 0.95)
                    img[y, x] = [255, 255, 255, brightness]
                else:
                    img[y, x] = [255, 255, 255, 0]
            else:
                img[y, x] = [0, 0, 0, 0]
    
    return Image.fromarray(img, 'RGBA')

# Generate all three maps using config values
print("Generating displacement and specular maps...")
print(f"Map size: {MAP_WIDTH}x{MAP_HEIGHT}, Selector: {SELECTOR_WIDTH}x{SELECTOR_HEIGHT}")

# 1. Magnification map (center zoom)
magnify_map, mag_max_disp = generate_magnification_map(MAP_WIDTH, MAP_HEIGHT, CORNER_RADIUS)
magnify_map.save('public/liquid-glass-magnify.png')
print(f"✅ Generated magnification map ({MAP_WIDTH}x{MAP_HEIGHT}) with max displacement: {mag_max_disp:.2f}px")

# 2. Bezel refraction map (edge distortion)
displacement_map, max_disp = generate_displacement_map_proper(MAP_WIDTH, MAP_HEIGHT, CORNER_RADIUS, BEZEL_WIDTH_FRACTION)
displacement_map.save('public/liquid-glass-displacement.png')
print(f"✅ Generated bezel displacement map ({MAP_WIDTH}x{MAP_HEIGHT}) with max displacement: {max_disp:.2f}px")

# 3. Specular highlight
specular_map = generate_specular_map(MAP_WIDTH, MAP_HEIGHT, CORNER_RADIUS, SPECULAR_ANGLE)
specular_map.save('public/liquid-glass-specular.png')
print(f"✅ Generated specular map with smooth gradient at {SPECULAR_ANGLE}° angle")
