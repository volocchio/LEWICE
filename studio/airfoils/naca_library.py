"""
NACA Airfoil Generator
Generate 4-digit NACA airfoil coordinates for LEWICE input.
"""
import math

def naca4(designation, n_points=60):
    designation = designation.strip()
    if not designation.isdigit() or len(designation) not in (4, 5):
        raise ValueError(f"Unsupported NACA designation: {designation}")

    # 4-digit series: MPXX (camber, camber position, thickness)
    # 5-digit series handling here is approximate for camber line, but thickness
    # is correctly taken from the final two digits (e.g. 23012 -> 12% thickness).
    m = int(designation[0]) / 100.0
    p = int(designation[1]) / 10.0
    t = int(designation[-2:]) / 100.0
    beta = [i * math.pi / (n_points - 1) for i in range(n_points)]
    x_coords = [0.5 * (1 - math.cos(b)) for b in beta]
    def thickness(x):
        return 5*t*(0.2969*math.sqrt(x)-0.1260*x-0.3516*x**2+0.2843*x**3-0.1015*x**4)
    def camber(x):
        if p == 0: return 0.0, 0.0
        if x < p:
            yc = m/p**2*(2*p*x - x**2)
            dyc = 2*m/p**2*(p - x)
        else:
            yc = m/(1-p)**2*((1-2*p)+2*p*x - x**2)
            dyc = 2*m/(1-p)**2*(p - x)
        return yc, dyc
    upper, lower = [], []
    for x in x_coords:
        yt = thickness(x)
        yc, dyc = camber(x)
        theta = math.atan(dyc) if dyc != 0 else 0
        upper.append((x - yt*math.sin(theta), yc + yt*math.cos(theta)))
        lower.append((x + yt*math.sin(theta), yc - yt*math.cos(theta)))
    return list(reversed(lower)) + upper[1:]

def write_xyd(filepath, coords):
    with open(filepath, "w") as f:
        for x, y in coords:
            f.write(f"   {x:.6f}    {y:.6f}\n")
    return filepath

COMMON_AIRFOILS = {
    "NACA 0012": "0012", "NACA 0015": "0015", "NACA 0018": "0018",
    "NACA 2412": "2412", "NACA 2415": "2415", "NACA 4412": "4412",
    "NACA 4415": "4415", "NACA 23012": "23012",
}
