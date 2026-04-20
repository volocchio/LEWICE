"""
LEWICE Output Parser
Reads LEWICE output .dat files and extracts ice shapes, beta, heat transfer, etc.
"""
import re
import os


def parse_ice_shape(filepath):
    """Parse an ice shape .dat file (e.g., shape.dat or final shape).
    Returns list of (x, y) tuples representing the iced airfoil surface.
    """
    coords = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    x = float(parts[0])
                    y = float(parts[1])
                    coords.append((x, y))
                except ValueError:
                    continue
    return coords


def parse_clean_airfoil(filepath):
    """Parse a .xyd geometry file.
    Returns list of (x, y) tuples for the clean airfoil.
    """
    coords = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    x = float(parts[0])
                    y = float(parts[1])
                    coords.append((x, y))
                except ValueError:
                    continue
    return coords


def parse_beta(filepath):
    """Parse collection efficiency (beta) output.
    Returns list of dicts with s, beta, x, y keys.
    """
    data = []
    with open(filepath, "r") as f:
        header_found = False
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "BETA" in line.upper() or "COLLECTION" in line.upper():
                header_found = True
                continue
            if header_found:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        vals = [float(p) for p in parts]
                        if len(vals) >= 4:
                            data.append({"s": vals[0], "beta": vals[1], "x": vals[2], "y": vals[3]})
                        elif len(vals) >= 2:
                            data.append({"s": vals[0], "beta": vals[1]})
                    except ValueError:
                        continue
    return data


def find_output_files(case_dir):
    """Scan a case output directory and categorize available files."""
    files = {}
    if not os.path.isdir(case_dir):
        return files
    for f in os.listdir(case_dir):
        fl = f.lower()
        if "shape" in fl and fl.endswith(".dat"):
            files["ice_shape"] = os.path.join(case_dir, f)
        elif "beta" in fl and fl.endswith(".dat"):
            files["beta"] = os.path.join(case_dir, f)
        elif "heat" in fl and fl.endswith(".dat"):
            files["heat_transfer"] = os.path.join(case_dir, f)
        elif "thick" in fl and fl.endswith(".dat"):
            files["thickness"] = os.path.join(case_dir, f)
    return files


def compute_ice_metrics(clean_coords, ice_coords):
    """Compute basic ice accretion metrics.
    Returns dict with max_thickness, upper_impingement, lower_impingement, etc.
    """
    if not clean_coords or not ice_coords:
        return {}

    # Simple max displacement calculation
    max_disp = 0.0
    for ix, iy in ice_coords:
        for cx, cy in clean_coords:
            if abs(ix - cx) < 0.002:
                disp = abs(iy - cy)
                if disp > max_disp:
                    max_disp = disp
                break

    return {
        "max_ice_thickness": max_disp,
        "ice_shape_points": len(ice_coords),
        "clean_airfoil_points": len(clean_coords),
    }


if __name__ == "__main__":
    # Quick test with case1 geometry
    coords = parse_clean_airfoil("../Inputs/case1.xyd")
    print(f"Clean airfoil: {len(coords)} points")
    print(f"LE region: x={coords[0][0]:.4f} to x={coords[-1][0]:.4f}")
