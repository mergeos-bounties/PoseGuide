import math

def calculate_pose_placement(background_width: int, background_height: int, horizon_y: int, pose_joints: dict, margin: int = 20) -> dict:
    """
    Calculates silhouette / stick figure placement bounding box respecting horizon and safe margins.
    """
    if background_width <= 0 or background_height <= 0:
        raise ValueError("Invalid background dimensions.")
    if horizon_y < 0 or horizon_y > background_height:
        raise ValueError("Horizon Y out of bounds.")
        
    scale_factor = (background_height - horizon_y) / float(background_height)
    bbox_width = int((background_width * 0.3) * max(scale_factor, 0.4))
    bbox_height = int((background_height * 0.6) * max(scale_factor, 0.4))

    # Center horizontally with safe margin constraint
    center_x = background_width // 2
    min_x = max(margin, center_x - bbox_width // 2)
    max_x = min(background_width - margin, center_x + bbox_width // 2)
    min_y = max(margin, horizon_y)
    max_y = min(background_height - margin, horizon_y + bbox_height)

    return {
        "placement_box": {"x_min": min_x, "x_max": max_x, "y_min": min_y, "y_max": max_y},
        "scale": scale_factor,
        "fits_safe_margin": (min_x >= margin and max_x <= background_width - margin and max_y <= background_height - margin)
    }
