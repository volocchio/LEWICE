"""
LEWICE Output Parser
Reads LEWICE output files and extracts ice shapes, collection efficiency,
heat transfer, impingement limits, and ice metrics.

Column layouts were checked against a LEWICE 3.2 Example 1 run:

  beta.dat:  s/c  beta  sle/c  x/c  y/c
  htc.dat:   seg  s/c   htc    fr
  thick.dat: xsav/c  ysav/c  ditot/c  area/c^2  s/c
  imp.dat:   size  xlow  ylow  slow  slowle  xhi  yhi  shi  shile
  limit.dat: xlow/c ylow/c slow/c xhi/c yhi/c shi/c
  final1.dat: x/c  y/c   (iced body, chord-normalized)
"""
import math
import os
import re


_FLOAT_RE = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?")
_MAX_THICK_RE = re.compile(
    r"Max\.\s*ice thickness\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?)",
    re.IGNORECASE,
)


def _floats(line):
    try:
        return [float(tok) for tok in line.split()]
    except ValueError:
        return None


def _iter_numeric_rows(filepath):
    """Yield (line_index, floats) for data rows. Header lines are skipped."""
    with open(filepath, "r", errors="replace") as f:
        for i, line in enumerate(f):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if any(c.isalpha() for c in stripped.replace("E", "").replace("e", "").replace("D", "").replace("d", "")):
                # Header (BETA, s/c, seg, ...). Fortran exponents are not headers.
                continue
            vals = _floats(stripped.replace("D", "E").replace("d", "e"))
            if vals:
                yield i, vals


def parse_ice_shape(filepath):
    """Parse an ice-shape file (final1.dat / ice*.dat).

    Returns a list of (x/c, y/c) tuples for the iced contour.
    """
    coords = []
    for _, vals in _iter_numeric_rows(filepath):
        if len(vals) >= 2:
            coords.append((vals[0], vals[1]))
    return coords


def parse_clean_airfoil(filepath):
    """Parse a .xyd (or other whitespace/comma) geometry file.

    Returns a list of (x, y) tuples. Non-numeric header lines are ignored.
    """
    coords = []
    with open(filepath, "r", errors="replace") as f:
        text = f.read()
    coords, _errors = parse_xy_text(text)
    return coords


def parse_xy_text(text):
    """Parse free-form x,y text. Accepts space, comma, or tab separators.

    Returns (coords, errors). Comments (#, //) and blank lines are ignored.
    """
    coords = []
    errors = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//") or line.startswith("!"):
            continue
        cleaned = line.replace(",", " ").replace("\t", " ").replace(";", " ")
        parts = cleaned.split()
        if len(parts) < 2:
            errors.append(f"line {lineno}: need at least 2 numbers, got '{raw.strip()}'")
            continue
        try:
            coords.append((float(parts[0]), float(parts[1])))
        except ValueError:
            errors.append(f"line {lineno}: not numeric -> '{raw.strip()}'")
    return coords, errors


def parse_beta(filepath):
    """Parse collection efficiency.

    Returns a list of time-step blocks. Each block is a list of dicts with
    keys s, beta, sle, x, y (x/y omitted when the file has only two columns).
    """
    rows = []
    for _, vals in _iter_numeric_rows(filepath):
        if len(vals) >= 5:
            rows.append({
                "s": vals[0], "beta": vals[1], "sle": vals[2],
                "x": vals[3], "y": vals[4],
            })
        elif len(vals) >= 2:
            rows.append({"s": vals[0], "beta": vals[1]})
    if not rows:
        return []
    if "s" in rows[0]:
        return _split_wrapped_blocks(rows, index_key="s")
    return [rows]


def _split_wrapped_blocks(rows, index_key):
    blocks = [[rows[0]]]
    for prev, cur in zip(rows, rows[1:]):
        if cur[index_key] < prev[index_key] - 0.4:
            blocks.append([cur])
        else:
            blocks[-1].append(cur)
    return blocks


def parse_htc(filepath):
    """Parse htc.dat. Returns a list of time-step blocks of {seg, s, htc, fr}."""
    rows = []
    for _, vals in _iter_numeric_rows(filepath):
        if len(vals) >= 4:
            rows.append({"seg": vals[0], "s": vals[1], "htc": vals[2], "fr": vals[3]})
        elif len(vals) >= 3:
            rows.append({"s": vals[0], "htc": vals[1], "fr": vals[2]})
    if not rows:
        return []
    # Segment numbers restart each time step; fall back to s-wrap.
    if "seg" in rows[0]:
        blocks = [[rows[0]]]
        for prev, cur in zip(rows, rows[1:]):
            if cur["seg"] < prev["seg"]:
                blocks.append([cur])
            else:
                blocks[-1].append(cur)
        return blocks
    return _split_wrapped_blocks(rows, index_key="s")


def parse_thickness(filepath):
    """Parse thick.dat. ditot is ice thickness normalized by chord."""
    rows = []
    for _, vals in _iter_numeric_rows(filepath):
        if len(vals) >= 5:
            rows.append({
                "x": vals[0], "y": vals[1], "ditot": vals[2],
                "area": vals[3], "s": vals[4],
            })
    return _split_wrapped_blocks(rows, index_key="s") if rows else []


def parse_impingement(filepath):
    """Parse imp.dat rows (one per icing step, usually).

    xlow/ylow/slow is the lower-surface limit (negative wrap coordinate).
    xhi/yhi/shi is the upper-surface limit.
    """
    rows = []
    for _, vals in _iter_numeric_rows(filepath):
        if len(vals) >= 9:
            rows.append({
                "mvd_um": vals[0],
                "lower": {"x": vals[1], "y": vals[2], "s": vals[3], "s_le": vals[4]},
                "upper": {"x": vals[5], "y": vals[6], "s": vals[7], "s_le": vals[8]},
            })
        elif len(vals) >= 8:
            rows.append({
                "lower": {"x": vals[0], "y": vals[1], "s": vals[2]},
                "upper": {"x": vals[4], "y": vals[5], "s": vals[6]},
            })
    return rows


def parse_limits(filepath):
    """Parse limit.dat icing-limit rows. Same lower/upper convention as imp.dat."""
    rows = []
    for _, vals in _iter_numeric_rows(filepath):
        if len(vals) >= 6:
            rows.append({
                "lower": {"x": vals[0], "y": vals[1], "s": vals[2]},
                "upper": {"x": vals[3], "y": vals[4], "s": vals[5]},
            })
    return rows


def parse_reported_thickness(log_text):
    """Return the final 'Max. ice thickness' value printed by LEWICE, in x/c.

    LEWICE prints one value per icing step and often wraps the number onto
    the next line. The last value is the one for the finished exposure.
    """
    if not log_text:
        return None
    matches = _MAX_THICK_RE.findall(log_text)
    if not matches:
        return None
    try:
        return float(matches[-1])
    except ValueError:
        return None


def find_output_files(case_dir):
    """Scan a case output directory and categorize available files."""
    files = {}
    if not os.path.isdir(case_dir):
        return files
    named = {
        "beta.dat": "beta",
        "htc.dat": "heat_transfer",
        "thick.dat": "thickness",
        "imp.dat": "impingement",
        "limit.dat": "limits",
        "final1.dat": "ice_shape",
        "lewice_stdout.txt": "log",
    }
    for fname in os.listdir(case_dir):
        key = named.get(fname.lower())
        if key:
            files[key] = os.path.join(case_dir, fname)
            continue
        fl = fname.lower()
        if fl.endswith(".dat"):
            if "shape" in fl or fl.startswith("final"):
                files.setdefault("ice_shape", os.path.join(case_dir, fname))
            elif "beta" in fl:
                files.setdefault("beta", os.path.join(case_dir, fname))
            elif "htc" in fl or "heat" in fl:
                files.setdefault("heat_transfer", os.path.join(case_dir, fname))
            elif "thick" in fl:
                files.setdefault("thickness", os.path.join(case_dir, fname))
    return files


def _dist_point_seg(px, py, ax, ay, bx, by):
    abx, aby = bx - ax, by - ay
    ab2 = abx * abx + aby * aby
    if ab2 <= 1e-20:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * abx + (py - ay) * aby) / ab2
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    return math.hypot(px - (ax + t * abx), py - (ay + t * aby))


def geometric_ice_thickness(clean_coords, ice_coords):
    """Maximum distance from an iced-contour point to the clean contour, in x/c.

    This is a fallback for when thick.dat is absent. It is the nearest-point
    distance, which is close to LEWICE's normal thickness for modest ice and
    can run a little high on a long horn.
    """
    if not clean_coords or not ice_coords or len(clean_coords) < 2:
        return 0.0, None
    max_d = 0.0
    at = None
    n = len(clean_coords)
    for px, py in ice_coords:
        best = None
        for i in range(n - 1):
            d = _dist_point_seg(px, py, clean_coords[i][0], clean_coords[i][1],
                                clean_coords[i + 1][0], clean_coords[i + 1][1])
            if best is None or d < best:
                best = d
        # Close the clean contour if the file itself is not closed.
        d = _dist_point_seg(px, py, clean_coords[-1][0], clean_coords[-1][1],
                            clean_coords[0][0], clean_coords[0][1])
        if best is None or d < best:
            best = d
        if best > max_d:
            max_d = best
            at = (px, py)
    return max_d, at


def _clean_leading_edge(clean_coords, ice_coords):
    pts = clean_coords or ice_coords or []
    if not pts:
        return (0.0, 0.0)
    return min(pts, key=lambda p: p[0])


def _nearest_clean_distance(px, py, clean_coords):
    best = None
    n = len(clean_coords)
    for i in range(n):
        j = 0 if i == n - 1 else i + 1
        d = _dist_point_seg(
            px, py,
            clean_coords[i][0], clean_coords[i][1],
            clean_coords[j][0], clean_coords[j][1],
        )
        if best is None or d < best:
            best = d
    return best if best is not None else 0.0


def horn_from_shape(clean_coords, ice_coords, nose_chord_fraction=0.35):
    """Geometric horn location on the iced contour.

    The horn location is the iced-contour point with the greatest standoff
    from the clean airfoil, inside the nose region. That matches the
    validation reports' "angle at maximum thickness" more closely than the
    foremost point, which can sit on a different horn. The angle is measured
    from the chord-forward direction (−x): 0° is straight ahead, positive is
    toward the upper surface.

    This is not the inscribed-cylinder horn angle in NASA/CR-1999-208690.
    It is a reproducible reading of the shape file LEWICE wrote.
    """
    if not ice_coords:
        return None
    x_le, y_le = _clean_leading_edge(clean_coords, ice_coords)
    use_distance = bool(clean_coords) and len(clean_coords) >= 2
    scored = []
    for x, y in ice_coords:
        radius = math.hypot(x - x_le, y - y_le)
        if x > x_le + nose_chord_fraction and radius > nose_chord_fraction:
            continue
        dist = _nearest_clean_distance(x, y, clean_coords) if use_distance else radius
        scored.append((x, y, radius, dist))
    if not scored:
        x, y = min(ice_coords, key=lambda p: (p[0], abs(p[1])))
        radius = math.hypot(x - x_le, y - y_le)
    else:
        # Greatest standoff, not greatest distance from the leading edge.
        # A lower-surface station is already far from the leading edge even
        # with no ice, so a radius test picks the bare airfoil.
        x, y, radius, _dist = max(scored, key=lambda p: p[3])
    angle = math.degrees(math.atan2(y - y_le, x_le - x))
    return {
        "x": x,
        "y": y,
        "radius_c": radius,
        "angle_deg": angle,
        "le_x": x_le,
        "le_y": y_le,
    }


def _beta_peak(block):
    if not block:
        return None
    row = max(block, key=lambda r: r["beta"])
    return row


def analyze_case(case_dir, clean_coords=None, chord_m=1.0, temp_c=None, log_text=None):
    """Collect the metrics the studio shows for one finished case.

    Thickness prefers thick.dat (ditot/c), which is LEWICE's own ice height.
    Chord-normalized coordinates are converted with ``chord_m`` (meters) to mm.
    """
    files = find_output_files(case_dir)
    warnings = []
    metrics = {
        "max_thickness_c": None,
        "max_thickness_mm": None,
        "thickness_source": None,
        "lewice_log_thickness_c": None,
        "horn_angle_deg": None,
        "horn_x": None,
        "horn_y": None,
        "horn_radius_c": None,
        "beta_max": None,
        "beta_max_s": None,
        "beta_max_x": None,
        "beta_max_y": None,
        "beta_min": None,
        "impingement": None,
        "impingement_source": None,
        "warnings": warnings,
        "files": files,
    }

    if log_text is None and files.get("log") and os.path.isfile(files["log"]):
        with open(files["log"], "r", errors="replace") as f:
            log_text = f.read()
    reported = parse_reported_thickness(log_text or "")
    if reported is not None:
        metrics["lewice_log_thickness_c"] = reported

    thick_blocks = []
    if files.get("thickness"):
        thick_blocks = parse_thickness(files["thickness"])
    if thick_blocks:
        last = thick_blocks[-1]
        peak = max(last, key=lambda r: r["ditot"])
        metrics["max_thickness_c"] = peak["ditot"]
        metrics["thickness_source"] = "thick.dat ditot/c"
        if reported is not None and reported > 0 and abs(peak["ditot"] - reported) / reported > 0.15:
            warnings.append(
                f"thick.dat max ditot/c ({peak['ditot']:.4f}) differs from the "
                f"LEWICE log value ({reported:.4f}) by more than 15%."
            )
    elif reported is not None:
        metrics["max_thickness_c"] = reported
        metrics["thickness_source"] = "LEWICE log"

    ice = []
    if files.get("ice_shape"):
        ice = parse_ice_shape(files["ice_shape"])
    if metrics["max_thickness_c"] is None and ice:
        geom_c, _at = geometric_ice_thickness(clean_coords, ice)
        metrics["max_thickness_c"] = geom_c
        metrics["thickness_source"] = "geometry (nearest clean surface)"
        warnings.append(
            "thick.dat was not found. Max thickness is the geometric distance "
            "from the iced contour to the clean airfoil, not LEWICE's ditot."
        )

    if metrics["max_thickness_c"] is not None:
        metrics["max_thickness_mm"] = metrics["max_thickness_c"] * float(chord_m) * 1000.0
        if metrics["max_thickness_c"] < 0:
            warnings.append("Ice thickness is negative, which is not physical.")

    horn = horn_from_shape(clean_coords, ice) if ice else None
    if horn:
        metrics["horn_angle_deg"] = horn["angle_deg"]
        metrics["horn_x"] = horn["x"]
        metrics["horn_y"] = horn["y"]
        metrics["horn_radius_c"] = horn["radius_c"]

    beta_blocks = parse_beta(files["beta"]) if files.get("beta") else []
    if beta_blocks:
        block = beta_blocks[-1]
        betas = [r["beta"] for r in block]
        peak = _beta_peak(block)
        metrics["beta_max"] = peak["beta"]
        metrics["beta_max_s"] = peak.get("s")
        metrics["beta_max_x"] = peak.get("x")
        metrics["beta_max_y"] = peak.get("y")
        metrics["beta_min"] = min(betas)
        n_hi = sum(1 for b in betas if b > 1.02)
        n_lo = sum(1 for b in betas if b < -0.01)
        if n_hi or n_lo:
            warnings.append(
                f"Collection efficiency left the physical range 0..1 "
                f"({n_lo} points < 0, {n_hi} points > 1.02)."
            )
        s_peak = peak.get("s")
        x_peak = peak.get("x")
        if s_peak is not None and abs(s_peak) > 0.25 and (x_peak is None or x_peak > 0.2):
            warnings.append(
                f"Beta peaks at s/c={s_peak:.3f}, away from the leading edge. "
                "On a clean or lightly iced airfoil the peak should sit near stagnation."
            )
    else:
        warnings.append("No beta.dat collection-efficiency output was found.")

    imp_rows = parse_impingement(files["impingement"]) if files.get("impingement") else []
    if imp_rows:
        metrics["impingement"] = {"upper": imp_rows[-1]["upper"], "lower": imp_rows[-1]["lower"]}
        metrics["impingement_source"] = "imp.dat final step"
    elif files.get("limits"):
        limit_rows = parse_limits(files["limits"])
        if limit_rows:
            metrics["impingement"] = {"upper": limit_rows[-1]["upper"], "lower": limit_rows[-1]["lower"]}
            metrics["impingement_source"] = "limit.dat final step"

    imp = metrics["impingement"]
    if imp:
        su = imp["upper"].get("s")
        sl = imp["lower"].get("s")
        if su is not None and sl is not None:
            # Wrap coordinate: upper limit should have the greater s.
            if su < sl:
                warnings.append(
                    "Impingement limits are reversed (upper s/c is less than lower s/c)."
                )
            if abs(su) > 0.6 or abs(sl) > 0.6:
                warnings.append(
                    "An impingement limit is aft of 60% chord. That is unusual for "
                    "Appendix C droplet sizes on a single-element airfoil."
                )

    if temp_c is not None and metrics["horn_angle_deg"] is not None:
        # Screening note only. Rime should stay near the stagnation line;
        # a large angle with a cold static temperature is worth a second look,
        # not an automatic rejection (AOA moves stagnation off the chord).
        if temp_c <= -20 and abs(metrics["horn_angle_deg"]) > 55:
            warnings.append(
                f"Static temperature is {temp_c:.1f} °C (rime regime) but the "
                f"outermost nose point sits {metrics['horn_angle_deg']:.0f}° off "
                "the chord-forward axis. Check angle of attack before treating this as glaze."
            )

    return metrics


def compute_ice_metrics(clean_coords, ice_coords, chord_m=1.0):
    """Backward-compatible summary used by older callers.

    Prefer analyze_case() when the LEWICE directory is available. This
    function no longer reports a vertical mismatch at similar x as "thickness";
    that missed ice that grows forward of the leading edge.
    """
    thick_c, _at = geometric_ice_thickness(clean_coords, ice_coords)
    horn = horn_from_shape(clean_coords, ice_coords)
    return {
        "max_ice_thickness": thick_c,
        "max_ice_thickness_mm": thick_c * float(chord_m) * 1000.0,
        "horn_angle_deg": None if not horn else horn["angle_deg"],
        "horn_x": None if not horn else horn["x"],
        "horn_y": None if not horn else horn["y"],
        "ice_shape_points": len(ice_coords or []),
        "clean_airfoil_points": len(clean_coords or []),
    }
