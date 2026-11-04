"""
NACA Airfoil Generator
Generate 4-digit and standard 5-digit NACA coordinates for LEWICE input.

5-digit camber uses the Abbott / von Doenhoff mean lines (not the 4-digit
formula with the digits regrouped). Thickness is the standard 4-digit
polynomial on the last two digits. The contour is closed: lower trailing
edge, around the leading edge, upper trailing edge, and back to the start.
Coordinates are chord-normalized.
"""
import math

# (m, k1) for non-reflex 5-digit camber, keyed by the first three digits.
_FIVE_DIGIT = {
    "210": (0.0580, 361.40, None),
    "220": (0.1260, 51.640, None),
    "230": (0.2025, 15.957, None),
    "240": (0.2900, 6.643, None),
    "250": (0.3910, 3.230, None),
    # Reflex mean lines: third value is k2/k1.
    "221": (0.1300, 51.990, 0.000764),
    "231": (0.2170, 15.793, 0.00677),
    "241": (0.3180, 6.520, 0.0303),
    "251": (0.4410, 3.191, 0.1355),
}


def _thickness(x, t):
    # a4 = -0.1015 is the classical open-trailing-edge coefficient.
    return 5 * t * (
        0.2969 * math.sqrt(max(x, 0.0))
        - 0.1260 * x
        - 0.3516 * x ** 2
        + 0.2843 * x ** 3
        - 0.1015 * x ** 4
    )


def _camber_4(x, m, p):
    if p == 0 or m == 0:
        return 0.0, 0.0
    if x < p:
        yc = m / p ** 2 * (2 * p * x - x ** 2)
        dyc = 2 * m / p ** 2 * (p - x)
    else:
        yc = m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x ** 2)
        dyc = 2 * m / (1 - p) ** 2 * (p - x)
    return yc, dyc


def _camber_5(x, m, k1, k2_over_k1):
    if k2_over_k1 is None:
        if x < m:
            yc = (k1 / 6.0) * (x ** 3 - 3 * m * x ** 2 + m ** 2 * (3 - m) * x)
            dyc = (k1 / 6.0) * (3 * x ** 2 - 6 * m * x + m ** 2 * (3 - m))
        else:
            yc = (k1 / 6.0) * m ** 3 * (1 - x)
            dyc = -(k1 / 6.0) * m ** 3
        return yc, dyc
    r = k2_over_k1
    if x < m:
        yc = (k1 / 6.0) * ((x - m) ** 3 - r * (1 - m) ** 3 * x - m ** 3 * x + m ** 3)
        dyc = (k1 / 6.0) * (3 * (x - m) ** 2 - r * (1 - m) ** 3 - m ** 3)
    else:
        yc = (k1 / 6.0) * (r * (x - m) ** 3 - r * (1 - m) ** 3 * x - m ** 3 * x + m ** 3)
        dyc = (k1 / 6.0) * (3 * r * (x - m) ** 2 - r * (1 - m) ** 3 - m ** 3)
    return yc, dyc


def naca_camber_kind(designation):
    """Return '4-digit', '5-digit', or '5-digit-reflex'."""
    designation = _normalize_designation(designation)
    if len(designation) == 4:
        return "4-digit"
    spec = _FIVE_DIGIT.get(designation[:3])
    if spec is None:
        raise ValueError(
            f"NACA {designation} is not a standard 5-digit section. "
            "Camber codes are 210, 220, 230, 240, 250 and reflex 221, 231, 241, 251."
        )
    return "5-digit-reflex" if spec[2] is not None else "5-digit"


def _normalize_designation(designation):
    designation = str(designation).strip().upper().replace("NACA", "").replace("-", "").replace(" ", "")
    if not designation.isdigit() or len(designation) not in (4, 5):
        raise ValueError(f"Unsupported NACA designation: {designation}")
    return designation


def naca4(designation, n_points=60):
    """Coordinates for a 4-digit or standard 5-digit NACA section.

    The name is historical: 5-digit designations are accepted too.
    ``n_points`` is the number of cosine stations from leading edge to
    trailing edge. The returned contour runs lower trailing edge -> leading
    edge -> upper trailing edge and is closed by repeating the first point.
    """
    designation = _normalize_designation(designation)
    t = int(designation[-2:]) / 100.0
    if len(designation) == 4:
        m = int(designation[0]) / 100.0
        p = int(designation[1]) / 10.0

        def camber(x):
            return _camber_4(x, m, p)
    else:
        spec = _FIVE_DIGIT.get(designation[:3])
        if spec is None:
            raise ValueError(
                f"NACA {designation} is not a standard 5-digit section. "
                "Camber codes are 210, 220, 230, 240, 250 and reflex 221, 231, 241, 251."
            )
        cm, k1, k2_over_k1 = spec

        def camber(x, cm=cm, k1=k1, k2_over_k1=k2_over_k1):
            return _camber_5(x, cm, k1, k2_over_k1)

    if n_points < 8:
        raise ValueError("n_points must be at least 8")
    beta = [i * math.pi / (n_points - 1) for i in range(n_points)]
    x_coords = [0.5 * (1 - math.cos(b)) for b in beta]
    upper, lower = [], []
    for x in x_coords:
        yt = _thickness(x, t)
        yc, dyc = camber(x)
        theta = math.atan(dyc) if dyc != 0 else 0.0
        upper.append((x - yt * math.sin(theta), yc + yt * math.cos(theta)))
        lower.append((x + yt * math.sin(theta), yc - yt * math.cos(theta)))
    # lower TE -> LE -> upper TE, then close back to lower TE.
    contour = list(reversed(lower)) + upper[1:]
    if contour[0] != contour[-1]:
        contour.append(contour[0])
    return contour


def max_thickness_fraction(coords):
    """Maximum y_upper - y_lower at a common x, as a fraction of chord."""
    if not coords:
        return 0.0
    # The generator stores lower (reversed) then upper, meeting at the LE
    # (minimum x). Split there.
    le_i = min(range(len(coords)), key=lambda i: coords[i][0])
    lower = coords[: le_i + 1]
    upper = coords[le_i:]
    best = 0.0
    for x, y_u in upper:
        # nearest lower point in x
        x_l, y_l = min(lower, key=lambda p: abs(p[0] - x))
        if abs(x_l - x) < 1e-6:
            best = max(best, y_u - y_l)
    return best


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
