"""
LEWICE Studio — Streamlit App
Modern UI for NASA LEWICE aircraft icing simulation.
No PhD in ice required.
"""
import re
import io as _io
import tempfile
import zipfile
import streamlit as st
import plotly.graph_objects as go
import json
import os
import sys
from datetime import datetime

# Add studio to path
sys.path.insert(0, os.path.dirname(__file__))

from lewice_engine.input_builder import (
    build_case_from_friendly, build_input, write_input,
    celsius_to_kelvin, ktas_to_ms, altitude_to_pressure, DEFAULTS
)
from lewice_engine.output_parser import (
    parse_clean_airfoil, parse_ice_shape, parse_beta, parse_htc,
    parse_xy_text, analyze_case,
)
from lewice_engine.runner import run_lewice, probe_lewice
from lewice_engine.plots import apply_equal_scale, leading_edge_points
from airfoils.naca_library import naca4, write_xyd, COMMON_AIRFOILS, naca_camber_kind
from reports.generator import build_report, build_pdf_report, _classify_ice, _assess_risk

APP_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(APP_DIR, ".."))
CUSTOM_SHAPES_PATH = os.path.join(APP_DIR, "airfoils", "custom_shapes.json")

_build_dt = datetime.fromtimestamp(os.path.getmtime(__file__))
BUILD_STAMP = _build_dt.strftime("Build %Y-%m-%d %H:%M:%S")

# ---------- Page Config ----------
st.set_page_config(
    page_title="LEWICE Studio",
    page_icon="<ice>",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.main-header { font-size: 2.5rem; font-weight: 700; color: #1a73e8; margin-bottom: 0; }
.sub-header { font-size: 1.1rem; color: #666; margin-bottom: 2rem; }
.risk-green { background: #e6f4ea; color: #1e7e34; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; }
.risk-yellow { background: #fff3cd; color: #856404; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; }
.risk-red { background: #f8d7da; color: #721c24; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">LEWICE Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Aircraft icing analysis made simple. Powered by NASA LEWICE 3.2.</p>', unsafe_allow_html=True)
st.caption(f"{BUILD_STAMP} | source: studio/app.py")
st.sidebar.caption(BUILD_STAMP)


EXAMPLE1_DIR = os.path.join(APP_DIR, "examples", "case1")

# NASA LEWICE distribution Example 1 (Inputs/case1.inp): a warm glaze case on
# the supplied NACA 0012-family geometry. Pressure is the file's 100000 Pa,
# which is not the ISA pressure at the sidebar's default altitude.
DEMO_CASE = {
    "airfoil_name": "LEWICE Example 1 geometry",
    "chord_m": 0.9144,
    "conditions": {
        "speed_ktas": 90.0 / (1852.0 / 3600.0),
        "speed_ms": 90.0,
        "altitude_ft": None,
        "pressure_pa": 100000.0,
        "temp_c": 268.30 - 273.15,
        "lwc": 0.54,
        "mvd": 20.0,
        "exposure_min": 6.0,
        "aoa_deg": 4.5,
    },
}


def _demo_sources():
    demo_xyd = os.path.join(EXAMPLE1_DIR, "case.xyd")
    if not os.path.isfile(demo_xyd):
        demo_xyd = os.path.join(REPO_ROOT, "Inputs", "case1.xyd")
    demo_ice = os.path.join(EXAMPLE1_DIR, "final1.dat")
    if not os.path.isfile(demo_ice):
        demo_ice = None
    return demo_xyd, demo_ice


def _current_inputs(airfoil_label, chord, aoa, speed_ktas, altitude_ft, temp_c, lwc, mvd, exposure_min):
    return {
        "airfoil": airfoil_label,
        "chord_m": round(float(chord), 6),
        "aoa_deg": float(aoa),
        "speed_ktas": float(speed_ktas),
        "altitude_ft": float(altitude_ft),
        "temp_c": float(temp_c),
        "lwc": float(lwc),
        "mvd": float(mvd),
        "exposure_min": float(exposure_min),
    }


def _inputs_differ(saved, current):
    if not saved:
        return False
    for key, value in current.items():
        other = saved.get(key)
        if isinstance(value, float):
            if other is None or abs(float(other) - value) > 1e-6:
                return True
        elif other != value:
            return True
    return False


def _format_conditions(inputs):
    if not inputs:
        return ""
    alt = inputs.get("altitude_ft")
    alt_txt = "n/a" if alt is None else f"{float(alt):.0f} ft"
    return (
        f"{inputs.get('airfoil', '')}, chord {float(inputs.get('chord_m', 0)):.4f} m, "
        f"AOA {float(inputs.get('aoa_deg', 0)):.1f}°, "
        f"{float(inputs.get('speed_ktas', 0)):.1f} KTAS, {alt_txt}, "
        f"{float(inputs.get('temp_c', 0)):.2f} °C, "
        f"LWC {float(inputs.get('lwc', 0)):.3f} g/m³, "
        f"MVD {float(inputs.get('mvd', 0)):.1f} µm, "
        f"{float(inputs.get('exposure_min', 0)):.2f} min"
    )


def _remember_run(output_dir, xyd_path=None):
    if "saved_runs" not in st.session_state:
        st.session_state["saved_runs"] = []

    final_path = os.path.join(output_dir, "final1.dat")
    if not os.path.isfile(final_path):
        return

    existing = [r for r in st.session_state["saved_runs"] if r.get("output_dir") == output_dir]
    if existing:
        return

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state["saved_runs"].insert(
        0,
        {
            "label": f"Run {stamp}",
            "output_dir": output_dir,
            "final_path": final_path,
            "xyd_path": xyd_path,
        },
    )


def _load_custom_shape_library(path=CUSTOM_SHAPES_PATH):
    """Load named custom 2-D shape presets from JSON.

    JSON format:
      {
        "Preset Name": [[x1, y1], [x2, y2], ...],
        ...
      }
    """
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return {}

    presets = {}
    if not isinstance(raw, dict):
        return presets
    for name, pts in raw.items():
        if not isinstance(name, str) or not isinstance(pts, list):
            continue
        cleaned = []
        for p in pts:
            if not isinstance(p, (list, tuple)) or len(p) < 2:
                continue
            try:
                cleaned.append((float(p[0]), float(p[1])))
            except (TypeError, ValueError):
                continue
        if len(cleaned) >= 3:
            presets[name] = cleaned
    return presets


def _points_to_text(points):
    return "\n".join(f"{x:.6f} {y:.6f}" for x, y in points)


def _new_output_subdir(root_dir, prefix):
    """Create a timestamped output subdirectory under a user-selected root."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.join(root_dir, f"{prefix}_{stamp}")
    candidate = base
    idx = 1
    while os.path.exists(candidate):
        candidate = f"{base}_{idx:02d}"
        idx += 1
    os.makedirs(candidate, exist_ok=False)
    return candidate


def _write_geometry_for_run(xyd_path, airfoil_choice, designation, custom_points, uploaded_xyd):
    """Write the .xyd file for a run based on current sidebar selection.
    Returns (ok: bool, message: str)."""
    if airfoil_choice == "Custom Point Array (2-D shape)":
        if not custom_points:
            return False, "No valid custom points to write."
        pts = list(custom_points)
        if (
            abs(pts[0][0] - pts[-1][0]) > 1e-9
            or abs(pts[0][1] - pts[-1][1]) > 1e-9
        ):
            pts.append(pts[0])
        write_xyd(xyd_path, pts)
        return True, "custom points"
    elif airfoil_choice == "Upload Custom .xyd":
        if not uploaded_xyd:
            return False, "Upload a .xyd file first."
        content = uploaded_xyd.getvalue().decode("utf-8", errors="replace")
        coords, errors = parse_xy_text(content)
        if len(coords) < 3:
            detail = errors[0] if errors else "no numeric x,y rows"
            return False, f"The uploaded file is not a usable geometry ({detail})."
        write_xyd(xyd_path, coords)
        return True, "uploaded .xyd"
    else:
        if not designation:
            return False, "No valid NACA designation."
        foil_coords = naca4(designation, n_points=80)
        write_xyd(xyd_path, foil_coords)
        return True, f"NACA {designation}"


def _appendix_c_critical_points(envelope):
    """Pick AC 20-73A-style critical points from the Appendix C envelope JSON.

    For each family we pick:
      - Max-LWC point at warmest temp  (worst glaze potential)
      - Max-LWC point at coldest temp  (worst rime potential)
      - Max-MVD point                  (worst impingement aft)
      - Max-LWC point overall          (worst total mass)
    Duplicates are removed.
    """
    selected = []
    for family_name, key in [("Continuous Max", "conditions"),
                             ("Intermittent Max", "intermittent_maximum")]:
        rows = envelope.get(key, [])
        if not rows:
            continue
        warm_t = max(r["temp_c"] for r in rows)
        cold_t = min(r["temp_c"] for r in rows)
        warm_pool = [r for r in rows if r["temp_c"] == warm_t]
        cold_pool = [r for r in rows if r["temp_c"] == cold_t]
        picks = {
            "warm-end max LWC": max(warm_pool, key=lambda r: r["lwc"]),
            "cold-end max LWC": max(cold_pool, key=lambda r: r["lwc"]),
            "max MVD":          max(rows, key=lambda r: (r["mvd"], r["lwc"])),
            "overall max LWC":  max(rows, key=lambda r: r["lwc"]),
        }
        seen = set()
        for rationale, row in picks.items():
            key_t = (row["altitude_ft"], row["temp_c"], row["lwc"], row["mvd"], row["exposure_min"])
            if key_t in seen:
                continue
            seen.add(key_t)
            selected.append({
                "family": family_name,
                "rationale": rationale,
                **row,
            })
    return selected


def _zip_dir_to_bytes(dir_path):
    """Return an in-memory zip of all files under dir_path."""
    buf = _io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(dir_path):
            for fname in files:
                full = os.path.join(root, fname)
                arcname = os.path.relpath(full, start=dir_path)
                zf.write(full, arcname)
    return buf.getvalue()


def _run_sweep(cases, airfoil_choice, designation, custom_points, uploaded_xyd,
               airfoil_label, chord_m, aoa_deg, speed_ktas, output_root_dir,
               progress_cb=None):
    """Run a list of icing cases sequentially and return a list of result dicts."""
    sweep_dir = _new_output_subdir(output_root_dir, "lewice_sweep")
    xyd_path = os.path.join(sweep_dir, "geometry.xyd")
    ok, msg = _write_geometry_for_run(xyd_path, airfoil_choice, designation,
                                      custom_points, uploaded_xyd)
    if not ok:
        return [], msg

    # Cache the clean coords once so we can compute thickness without re-parsing.
    try:
        clean_coords_cached = parse_clean_airfoil(xyd_path)
    except Exception:
        clean_coords_cached = None

    results = []
    total = len(cases)
    for i, case in enumerate(cases, start=1):
        case_dir = os.path.join(sweep_dir, f"case_{i:02d}")
        os.makedirs(case_dir, exist_ok=True)
        inp_path = os.path.join(case_dir, "case.inp")
        case_xyd = os.path.join(case_dir, "case.xyd")
        # LEWICE writes outputs into the cwd / inp directory; copy xyd next to inp
        with open(xyd_path, "r") as src, open(case_xyd, "w") as dst:
            dst.write(src.read())

        params = build_case_from_friendly(
            chord_m=chord_m,
            aoa_deg=case.get("aoa_deg", aoa_deg),
            speed_ktas=case.get("speed_ktas", speed_ktas),
            altitude_ft=case.get("altitude_ft"),
            temp_c=case.get("temp_c"),
            lwc=case.get("lwc"),
            mvd=case.get("mvd"),
            exposure_min=case.get("exposure_min"),
        )
        title = f"{airfoil_label} - sweep case {i}"
        write_input(inp_path, params, title=title)

        if progress_cb:
            progress_cb(i - 1, total, case)

        run_result = run_lewice(inp_path, case_xyd, work_dir=case_dir)

        row = {
            "#": i,
            "family": case.get("family", "Custom"),
            "rationale": case.get("rationale", ""),
            "altitude_ft": case.get("altitude_ft"),
            "temp_C": case.get("temp_c"),
            "LWC_g_m3": case.get("lwc"),
            "MVD_um": case.get("mvd"),
            "exposure_min": case.get("exposure_min"),
            "AOA_deg": case.get("aoa_deg", aoa_deg),
            "status": run_result.get("status"),
            "elapsed_s": run_result.get("elapsed_seconds"),
            "max_ice_mm": None,
            "horn_deg": None,
            "beta_max": None,
            "ice_type": _classify_ice(case.get("temp_c", -10),
                                      case.get("lwc", 0.5),
                                      case.get("mvd", 20)),
            "risk": None,
            "output_dir": case_dir,
        }

        final_path = os.path.join(case_dir, "final1.dat")
        if run_result.get("status") == "success" and os.path.isfile(final_path):
            try:
                metrics = analyze_case(
                    case_dir,
                    clean_coords_cached,
                    chord_m=chord_m,
                    temp_c=case.get("temp_c"),
                    log_text=run_result.get("stdout"),
                )
                if metrics.get("max_thickness_mm") is not None:
                    row["max_ice_mm"] = round(metrics["max_thickness_mm"], 2)
                    risk_level, _ = _assess_risk(row["max_ice_mm"], row["ice_type"])
                    row["risk"] = risk_level
                if metrics.get("horn_angle_deg") is not None:
                    row["horn_deg"] = round(metrics["horn_angle_deg"], 1)
                if metrics.get("beta_max") is not None:
                    row["beta_max"] = round(metrics["beta_max"], 3)
            except Exception as exc:
                row["status"] = f"parse_error: {exc}"
        elif run_result.get("status") != "success":
            row["status"] = run_result.get("message") or run_result.get("status", "error")

        results.append(row)
        if progress_cb:
            progress_cb(i, total, case)

    return results, sweep_dir


def _collect_output_sources():
    candidates = []
    seen = set()

    def add_candidate(label, output_dir, xyd_path=None):
        final_path = os.path.join(output_dir, "final1.dat")
        if not os.path.isfile(final_path):
            return
        if output_dir in seen:
            return
        seen.add(output_dir)
        candidates.append(
            {
                "label": label,
                "output_dir": output_dir,
                "final_path": final_path,
                "xyd_path": xyd_path,
            }
        )

    last_run_dir = st.session_state.get("last_run_dir")
    if last_run_dir:
        add_candidate("Latest LEWICE run (this session)", last_run_dir, st.session_state.get("last_run_xyd"))

    for saved in st.session_state.get("saved_runs", []):
        add_candidate(saved.get("label", "Saved run"), saved["output_dir"], saved.get("xyd_path"))

    scan_roots = [
        os.path.join(REPO_ROOT, "results"),
        os.path.join(REPO_ROOT, "grid_examples"),
        os.path.join(APP_DIR, "test_run"),
    ]
    for root in scan_roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _, filenames in os.walk(root):
            if "final1.dat" in filenames:
                rel = os.path.relpath(dirpath, REPO_ROOT)
                add_candidate(f"Detected: {rel}", dirpath)

    return candidates

# ---------- Sidebar: Configuration ----------
st.sidebar.header("Aircraft & Flight Conditions")

# Airfoil selection
airfoil_choice = st.sidebar.selectbox(
    "Airfoil / Shape",
    list(COMMON_AIRFOILS.keys()) + [
        "Custom NACA Code",
        "Upload Custom .xyd",
        "Custom Point Array (2-D shape)",
    ],
    help=(
        "Pick a stock airfoil, enter a NACA code, upload a .xyd file, or paste a "
        "raw x,y point list. The point-array mode includes a preset dropdown for "
        "saved custom shapes and is intended for antenna fairings "
        "and other non-airfoil 2-D cross-sections."
    ),
)

designation = None
airfoil_label = airfoil_choice
airfoil_is_valid = True
custom_points = None  # list[tuple[float, float]] when point-array mode is active

if airfoil_choice in COMMON_AIRFOILS:
    designation = COMMON_AIRFOILS[airfoil_choice]
elif airfoil_choice == "Custom NACA Code":
    custom_naca = st.sidebar.text_input("NACA Code", value="23012", help="Examples: 2412, 4415, 23012")
    candidate = custom_naca.strip().upper().replace("NACA", "").replace("-", "").replace(" ", "")
    if re.fullmatch(r"\d{4}|\d{5}", candidate):
        try:
            kind = naca_camber_kind(candidate)
        except ValueError as exc:
            airfoil_is_valid = False
            st.sidebar.error(str(exc))
        else:
            designation = candidate
            airfoil_label = f"NACA {designation}"
            if kind == "5-digit":
                st.sidebar.caption("Standard 5-digit mean line. Thickness is the last two digits.")
            elif kind == "5-digit-reflex":
                st.sidebar.caption("Standard reflex 5-digit mean line. Thickness is the last two digits.")
    else:
        airfoil_is_valid = False
        st.sidebar.error("Enter a valid NACA code: 4 digits (e.g. 2412) or 5 digits (e.g. 23012).")

if designation:
    airfoil_label = f"NACA {designation}"

if airfoil_choice == "Upload Custom .xyd":
    uploaded_xyd = st.sidebar.file_uploader("Upload .xyd file", type=["xyd", "dat", "txt"])
else:
    uploaded_xyd = None


if airfoil_choice == "Custom Point Array (2-D shape)":
    custom_shape_library = _load_custom_shape_library()
    preset_options = ["(none)"] + list(custom_shape_library.keys())
    selected_preset = st.sidebar.selectbox(
        "Load saved shape preset",
        preset_options,
        help=(
            "Choose a preset from studio/airfoils/custom_shapes.json. Selecting a preset "
            "loads its points into the editable text area below."
        ),
    )
    if selected_preset != "(none)":
        if st.session_state.get("last_loaded_shape_preset") != selected_preset:
            st.session_state["custom_point_text"] = _points_to_text(custom_shape_library[selected_preset])
            st.session_state["last_loaded_shape_preset"] = selected_preset
            st.sidebar.success(f"Loaded preset: {selected_preset}")
    else:
        st.session_state["last_loaded_shape_preset"] = "(none)"

    if not custom_shape_library:
        st.sidebar.caption("No preset library loaded. Add studio/airfoils/custom_shapes.json to enable presets.")

    st.sidebar.caption(
        "Paste x y pairs (one per line). Coordinates should be in chord-normalized "
        "units (0..1 along x). LEWICE expects a closed loop traversed lower TE -> "
        "LE -> upper TE (same convention as .xyd)."
    )
    pts_uploaded = st.sidebar.file_uploader(
        "...or upload a CSV/TXT of points",
        type=["csv", "txt", "dat", "xyd"],
        key="custom_point_upload",
    )
    if pts_uploaded is not None:
        file_id = (pts_uploaded.name, pts_uploaded.size)
        if st.session_state.get("custom_point_upload_id") != file_id:
            try:
                st.session_state["custom_point_text"] = pts_uploaded.getvalue().decode("utf-8", errors="replace")
                st.session_state["custom_point_upload_id"] = file_id
            except Exception as exc:
                st.sidebar.error(f"Could not read uploaded file: {exc}")

    if "custom_point_text" not in st.session_state:
        st.session_state["custom_point_text"] = ""
    point_text = st.sidebar.text_area(
        "Point array (x  y per line)",
        height=220,
        placeholder="1.0  0.0\n0.5  -0.05\n0.0   0.0\n0.5   0.05\n1.0   0.0",
        key="custom_point_text",
    )

    parsed_coords, parse_errors = parse_xy_text(point_text or "")
    if parse_errors:
        airfoil_is_valid = False
        st.sidebar.error(
            "Point array has " + str(len(parse_errors)) + " issue(s):\n\n- "
            + "\n- ".join(parse_errors[:5])
            + ("\n- ..." if len(parse_errors) > 5 else "")
        )
    if not parsed_coords:
        airfoil_is_valid = False
        if not parse_errors:
            st.sidebar.info("Enter at least 3 (x, y) points to define a 2-D shape.")
    elif len(parsed_coords) < 3:
        airfoil_is_valid = False
        st.sidebar.error("Need at least 3 points to define a 2-D shape.")
    else:
        custom_points = parsed_coords
        airfoil_label = f"Custom 2-D Shape ({len(custom_points)} pts)"
        st.sidebar.success(f"Parsed {len(custom_points)} points.")

chord_in_input = st.sidebar.number_input("Chord Length (in)", value=36.0, min_value=0.5, max_value=1968.0, step=0.5)
chord = chord_in_input * 0.0254  # convert to meters for LEWICE
st.sidebar.caption(f"≈ {chord:.4f} m")
aoa = st.sidebar.number_input("Angle of Attack (deg)", value=0.0, min_value=-15.0, max_value=25.0, step=0.5)

st.sidebar.header("Flight Conditions")
speed_ktas = st.sidebar.number_input("Speed (KTAS)", value=175.0, min_value=50.0, max_value=600.0, step=5.0)
altitude_ft = st.sidebar.number_input("Altitude (ft)", value=10000, min_value=0, max_value=45000, step=500)
temp_c = st.sidebar.number_input("Temperature (C)", value=-10.0, min_value=-40.0, max_value=0.0, step=1.0)

st.sidebar.header(
    "Icing Conditions",
    help=(
        "Atmospheric icing parameters that drive ice accretion. The relevant "
        "certification reference is **14 CFR Part 25, Appendix C**, which defines "
        "the supercooled liquid water cloud envelopes an aircraft must be shown "
        "safe in."
    ),
)

envelope_mode = st.sidebar.radio(
    "Mode",
    ["Single Condition", "Appendix C Envelope", "Custom Batch"],
    help=(
        "**Single Condition** — one LEWICE case at the LWC/MVD/exposure below.\n\n"
        "**Appendix C Envelope** — sweep the FAA Part 25 App. C standard cloud set:\n"
        "  • *Continuous Maximum* (stratiform clouds, ~17.4 nm horizontal extent, "
        "lower LWC, longer exposure) — used for the long-duration hold case.\n"
        "  • *Intermittent Maximum* (cumuliform clouds, ~2.6 nm horizontal extent, "
        "higher LWC, shorter exposure) — used for the worst-case short encounter.\n\n"
        "**Custom Batch** — edit a table of cases and run them on this page."
    ),
)

MODE_HELP = {
    "Single Condition": "Run one LEWICE case using the exact LWC, MVD, and exposure values set below.",
    "Appendix C Envelope": "Preview and run against the FAA Appendix C standard condition set for certification-style sweeps.",
    "Custom Batch": "Run the cases in the table on the Run & Results tab. Blank cells are dropped; each remaining row is one LEWICE case.",
}
st.sidebar.caption(MODE_HELP[envelope_mode])

lwc = st.sidebar.number_input(
    "LWC (g/m3)", value=0.54, min_value=0.05, max_value=3.0, step=0.05,
    help=(
        "**Liquid Water Content** — mass of supercooled liquid water per cubic "
        "meter of cloud air. Drives how fast ice accretes. Appendix C continuous "
        "max ranges roughly 0.04–0.8 g/m³ (temp/altitude dependent); intermittent "
        "max can reach ~2.9 g/m³."
    ),
)
mvd = st.sidebar.number_input(
    "MVD (microns)", value=20.0, min_value=5.0, max_value=50.0, step=1.0,
    help=(
        "**Median Volume Diameter** — droplet size at which half the cloud's "
        "liquid water mass is in larger droplets and half in smaller. Appendix C "
        "covers 15–40 µm. Larger droplets impinge further aft and matter for "
        "protected-surface coverage. Beyond 40 µm you're into Appendix O "
        "(SLD/freezing drizzle), which LEWICE does not certify against."
    ),
)
exposure_min = st.sidebar.number_input(
    "Exposure Time (min)", value=6.0, min_value=0.5, max_value=45.0, step=0.5,
    help=(
        "How long the aircraft is in the icing cloud. Appendix C horizontal "
        "extents are converted to time using TAS — e.g. 17.4 nm continuous max "
        "at 175 KTAS ≈ 6 min; 2.6 nm intermittent max ≈ 0.9 min. Longer exposure "
        "= more ice; the LWC/exposure trade is built into the Appendix C curves."
    ),
)

st.sidebar.caption(
    "Per FAA acceptance of PSCP ST20857SE-A (Mar 20, 2026): critical LEWICE "
    "conditions to be developed per AC 20-73A guidance."
)

# ---------- Main Panel ----------
tab1, tab2, tab3, tab4 = st.tabs(["Airfoil Preview", "LEWICE Input", "Run & Results", "Report"])

# ---- Tab 1: Airfoil Preview ----
with tab1:
    st.subheader("Airfoil Geometry")

    if airfoil_choice != "Upload Custom .xyd" and airfoil_choice != "Custom Point Array (2-D shape)" and designation and airfoil_is_valid:
        coords = naca4(designation, n_points=80)
        x_vals = [c[0] for c in coords]
        y_vals = [c[1] for c in coords]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Clean Airfoil",
                                 line=dict(color="#1a73e8", width=2)))
        apply_equal_scale(fig, coords, uirevision=f"preview-{airfoil_label}-{len(coords)}")
        fig.update_layout(
            margin=dict(l=40, r=40, t=40, b=40),
            title=f"{airfoil_label} — {len(coords)} points",
        )
        st.plotly_chart(fig, width="stretch", config={"scrollZoom": True})

        col1, col2, col3 = st.columns(3)
        col1.metric("Points", len(coords))
        col2.metric("Max Thickness", f"{int(designation[-2:])}%")
        if len(designation) == 4:
            col3.metric("Max Camber", f"{int(designation[0])}%")
        else:
            col3.metric("Series", "5-digit")
    elif airfoil_choice == "Custom Point Array (2-D shape)":
        if custom_points and airfoil_is_valid:
            x_vals = [c[0] for c in custom_points]
            y_vals = [c[1] for c in custom_points]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_vals, y=y_vals,
                mode="lines+markers", name="Custom 2-D Shape",
                line=dict(color="#C8A84E", width=2),
                marker=dict(size=4),
            ))
            apply_equal_scale(
                fig, custom_points, x_title="x/c", y_title="y/c",
                uirevision=f"custom-{len(custom_points)}-{custom_points[0]}",
            )
            fig.update_layout(
                margin=dict(l=40, r=40, t=40, b=40),
                title=f"{airfoil_label}",
            )
            st.plotly_chart(fig, width="stretch", config={"scrollZoom": True})

            x_min, x_max = min(x_vals), max(x_vals)
            y_min, y_max = min(y_vals), max(y_vals)
            closed = (
                abs(custom_points[0][0] - custom_points[-1][0]) < 1e-6
                and abs(custom_points[0][1] - custom_points[-1][1]) < 1e-6
            )
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Points", len(custom_points))
            mc2.metric("X range", f"{x_min:.3f} → {x_max:.3f}")
            mc3.metric("Y range", f"{y_min:.3f} → {y_max:.3f}")
            mc4.metric("Closed loop", "Yes" if closed else "No")
            if not closed:
                st.warning(
                    "First and last point differ. LEWICE expects a closed contour — "
                    "the runner will auto-close the loop, but verify your shape is intentional."
                )
        else:
            st.info("Paste a point array in the sidebar to preview the 2-D shape.")
    else:
        if uploaded_xyd:
            content = uploaded_xyd.getvalue().decode("utf-8", errors="replace")
            coords, errors = parse_xy_text(content)
            if len(coords) < 3:
                st.error("Could not read at least 3 x,y points from that file.")
                if errors:
                    st.caption(errors[0])
            else:
                x_vals = [c[0] for c in coords]
                y_vals = [c[1] for c in coords]
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines",
                                         line=dict(color="#1a73e8", width=2)))
                apply_equal_scale(fig, coords, uirevision=f"upload-{len(coords)}")
                fig.update_layout(margin=dict(l=40, r=40, t=40, b=40), title="Uploaded geometry")
                st.plotly_chart(fig, width="stretch", config={"scrollZoom": True})
                st.metric("Points", len(coords))
                x_span = max(x_vals) - min(x_vals)
                if x_span < 0.5 or x_span > 2.0 or min(x_vals) < -0.2 or max(x_vals) > 1.5:
                    st.warning(
                        "These coordinates are not near a 0–1 chord. LEWICE treats the "
                        "file as chord-normalized (x/c, y/c). Scale the shape onto a unit chord before running."
                    )
        else:
            st.info("Upload a .xyd file to preview the airfoil geometry.")
    if airfoil_choice != "Upload Custom .xyd" and (not designation or not airfoil_is_valid):
        if airfoil_choice == "Custom Point Array (2-D shape)":
            pass  # already handled above
        else:
            st.warning("Enter a valid NACA code to preview geometry.")

# ---- Tab 2: LEWICE Input Preview ----
with tab2:
    st.subheader("Generated LEWICE Input File")

    params = build_case_from_friendly(
        chord_m=chord, aoa_deg=aoa,
        speed_ktas=speed_ktas, altitude_ft=altitude_ft,
        temp_c=temp_c, lwc=lwc, mvd=mvd,
        exposure_min=exposure_min,
    )
    inp_text = build_input(params, title=f"LEWICE Studio - {airfoil_label}")
    st.code(inp_text, language="fortran")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocity (m/s)", f"{params['VINF']:.1f}")
    col2.metric("Temperature (K)", f"{params['TINF']:.1f}")
    col3.metric("Pressure (Pa)", f"{params['PINF']:.0f}")
    col4.metric("Exposure (s)", f"{params['TSTOP']:.0f}")
    st.caption(
        f"Written for LEWICE as chord {params['CHORD']:.4f} m, "
        f"V {params['VINF']:.2f} m/s, T {params['TINF']:.2f} K, "
        f"P {params['PINF']:.0f} Pa, LWC {params['LWC']:.3f} g/m³, "
        f"MVD {params['DPD']:.1f} µm. "
        f"IFLO = {int(params['IFLO'])} icing updates "
        f"(about {params['TSTOP'] / max(int(params['IFLO']), 1):.0f} s each). "
        "IFLO is the number of flow updates, not a solver switch. NPL stays 24, as in the LEWICE examples."
    )

    if envelope_mode == "Appendix C Envelope":
        with st.expander("What is the Appendix C envelope?", expanded=False):
            st.markdown(
                """
**14 CFR Part 25, Appendix C** is the FAA's atmospheric icing design envelope
for transport-category aircraft certification. It defines two supercooled
liquid-water cloud families an aircraft must be shown safe to operate in:

- **Continuous Maximum (stratiform).** Layer-cloud icing. Lower LWC
  (~0.04–0.8 g/m³), broader horizontal extent (datum 17.4 nm, scaled by an
  extent factor for longer encounters), temperatures down to about −30 °C,
  altitudes up to ~22,000 ft. This is the **hold / cruise** case.
- **Intermittent Maximum (cumuliform).** Convective-cloud icing. Higher LWC
  (peaks ~2.9 g/m³), short horizontal extent (datum 2.6 nm), temperatures down
  to about −40 °C, altitudes up to ~22,000 ft. This is the **short, severe
  encounter** case.

Each family is a set of curves of LWC vs. MVD, parameterized by ambient
temperature and altitude (see Figures 1–6 of Appendix C). For a certification
credit, you sweep the airfoil through *critical points* on these curves —
typically the highest-LWC / largest-MVD combinations at the cold and warm ends
of the envelope — and show the ice protection system handles them.

Guidance for picking those critical points lives in **AC 20-73A** (Aircraft
Ice Protection), which is the document the FAA tied to the PSCP acceptance.

*Note: Appendix C does not cover Supercooled Large Droplets (freezing drizzle
/ freezing rain). Those are Part 25 **Appendix O**, and LEWICE 3.2 is not
validated for them.*
                """.strip()
            )
        env_path = os.path.join(os.path.dirname(__file__), "envelopes", "appendix_c.json")
        if os.path.isfile(env_path):
            with open(env_path, encoding="utf-8-sig") as f:
                envelope = json.load(f)
            st.info(
                f"Appendix C envelope loaded: {len(envelope['conditions'])} continuous "
                f"+ {len(envelope['intermittent_maximum'])} intermittent conditions",
                icon="ℹ️",
            )
            st.json(envelope["conditions"][:5])
            st.caption("Showing first 5 of " + str(len(envelope["conditions"])) + " conditions...")

# ---- Tab 3: Run & Results ----
with tab3:
    st.subheader("Run LEWICE")
    st.info(
        "Sweep controls are on this tab under 'Envelope / Batch Sweep Runner'. "
        "If you do not see that section, restart Streamlit from studio/app.py.",
        icon="ℹ️",
    )

    runtime = probe_lewice()
    if runtime["ok"]:
        st.success(runtime["message"])
    else:
        st.error(runtime["message"])

    # Server-side temp root — results are delivered via browser download
    output_root_dir = os.path.join(tempfile.gettempdir(), "lewice_studio")
    os.makedirs(output_root_dir, exist_ok=True)

    sidebar_inputs = _current_inputs(
        airfoil_label, chord, aoa, speed_ktas, altitude_ft, temp_c, lwc, mvd, exposure_min
    )

    run_disabled = (
        not runtime["ok"]
        or (
            airfoil_choice not in ("Upload Custom .xyd", "Custom Point Array (2-D shape)")
            and (not designation or not airfoil_is_valid)
        )
        or (airfoil_choice == "Custom Point Array (2-D shape)" and (not custom_points or not airfoil_is_valid))
        or (airfoil_choice == "Upload Custom .xyd" and uploaded_xyd is None)
    )
    if st.button("Run Single Case", disabled=run_disabled, type="primary"):
        st.info("Running LEWICE... a single case is usually a few seconds, longer when IFLO is high.")
        with st.spinner("Simulating ice accretion..."):
            tmp_dir = _new_output_subdir(output_root_dir, "lewice_single")
            inp_path = os.path.join(tmp_dir, "case.inp")
            xyd_path = os.path.join(tmp_dir, "case.xyd")

            write_input(inp_path, params, title=f"Studio Run - {airfoil_label}")

            ok, msg = _write_geometry_for_run(
                xyd_path, airfoil_choice, designation, custom_points, uploaded_xyd
            )
            if not ok:
                st.error(msg)
                st.stop()

            result = run_lewice(inp_path, xyd_path, work_dir=tmp_dir)

            if result["status"] == "success":
                st.success(result.get("message") or f"LEWICE completed in {result['elapsed_seconds']}s")
                st.session_state["last_run_dir"] = tmp_dir
                st.session_state["last_run_xyd"] = xyd_path
                st.session_state["last_run"] = {
                    "output_dir": tmp_dir,
                    "xyd_path": xyd_path,
                    "inputs": sidebar_inputs,
                    "airfoil_label": airfoil_label,
                }
                _remember_run(tmp_dir, xyd_path)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.session_state["last_zip_bytes"] = _zip_dir_to_bytes(tmp_dir)
                st.session_state["last_zip_name"] = f"lewice_run_{ts}.zip"
            else:
                st.error(result.get("message") or result.get("stderr") or "LEWICE failed.")

    if st.session_state.get("last_zip_bytes"):
        st.download_button(
            "Download results (.zip)",
            data=st.session_state["last_zip_bytes"],
            file_name=st.session_state.get("last_zip_name", "lewice_run.zip"),
            mime="application/zip",
            key="download_single_zip",
        )

    # ---------- Envelope / Batch Sweep ----------
    st.divider()
    st.subheader("Envelope / Batch Sweep Runner")
    if envelope_mode not in ("Appendix C Envelope", "Custom Batch"):
        st.info(
            "Sweep runner is enabled when sidebar Mode is set to 'Appendix C Envelope' "
            "or 'Custom Batch'.",
            icon="ℹ️",
        )
    else:
        st.caption(f"Active sweep mode: {envelope_mode}")

        env_path = os.path.join(os.path.dirname(__file__), "envelopes", "appendix_c.json")
        envelope = None
        if os.path.isfile(env_path):
            with open(env_path, encoding="utf-8-sig") as f:
                envelope = json.load(f)

        sweep_cases = []

        if envelope_mode == "Appendix C Envelope":
            if not envelope:
                st.error("Appendix C envelope JSON not found.")
            else:
                preset = st.radio(
                    "Sweep set",
                    [
                        "AC 20-73A critical points (recommended)",
                        "Continuous Maximum (full)",
                        "Intermittent Maximum (full)",
                        "Both families (full)",
                    ],
                    help=(
                        "**Critical points** — 4–8 cases per AC 20-73A guidance "
                        "(warm/cold-end max LWC, max MVD, overall max LWC) for each family. "
                        "This is what most certification programs actually run.\n\n"
                        "**Full** — every condition in the JSON. Useful for envelope coverage "
                        "plots but burns LEWICE time on redundant points."
                    ),
                )
                if preset == "AC 20-73A critical points (recommended)":
                    sweep_cases = _appendix_c_critical_points(envelope)
                elif preset == "Continuous Maximum (full)":
                    sweep_cases = [{"family": "Continuous Max", "rationale": "", **r}
                                   for r in envelope.get("conditions", [])]
                elif preset == "Intermittent Maximum (full)":
                    sweep_cases = [{"family": "Intermittent Max", "rationale": "", **r}
                                   for r in envelope.get("intermittent_maximum", [])]
                else:
                    sweep_cases = (
                        [{"family": "Continuous Max", "rationale": "", **r}
                         for r in envelope.get("conditions", [])]
                        + [{"family": "Intermittent Max", "rationale": "", **r}
                           for r in envelope.get("intermittent_maximum", [])]
                    )

                st.caption(
                    f"{len(sweep_cases)} case(s) queued. "
                    f"Speed/AOA/chord come from the sidebar; T, LWC, MVD, exposure, altitude come from the envelope."
                )
                st.dataframe(sweep_cases, width="stretch", hide_index=True)

        else:  # Custom Batch
            st.caption(
                "Edit the table below — one row per case. A row is skipped if temperature, "
                "LWC, MVD, or exposure is empty. Speed and chord always come from the sidebar."
            )
            default_rows = st.session_state.get("custom_batch_rows") or [
                {"temp_c": -10.0, "lwc": 0.54, "mvd": 20.0, "exposure_min": 6.0,
                 "altitude_ft": 10000, "aoa_deg": 0.0},
                {"temp_c": -20.0, "lwc": 0.30, "mvd": 25.0, "exposure_min": 6.0,
                 "altitude_ft": 15000, "aoa_deg": 0.0},
            ]
            edited = st.data_editor(
                default_rows,
                num_rows="dynamic",
                width="stretch",
                key="custom_batch_editor",
                column_config={
                    "temp_c": st.column_config.NumberColumn("Temp (°C)", step=1.0),
                    "lwc": st.column_config.NumberColumn("LWC (g/m³)", step=0.05, format="%.3f"),
                    "mvd": st.column_config.NumberColumn("MVD (µm)", step=1.0),
                    "exposure_min": st.column_config.NumberColumn("Exposure (min)", step=0.5),
                    "altitude_ft": st.column_config.NumberColumn("Altitude (ft)", step=500),
                    "aoa_deg": st.column_config.NumberColumn("AOA (deg)", step=0.5),
                },
            )
            sweep_cases = [
                {
                    "family": "Custom",
                    "rationale": f"row {i+1}",
                    "temp_c": row.get("temp_c"),
                    "lwc": row.get("lwc"),
                    "mvd": row.get("mvd"),
                    "exposure_min": row.get("exposure_min"),
                    "altitude_ft": row.get("altitude_ft"),
                    "aoa_deg": row.get("aoa_deg", aoa),
                }
                for i, row in enumerate(edited)
                if row.get("temp_c") is not None and row.get("lwc") is not None
                and row.get("mvd") is not None and row.get("exposure_min") is not None
            ]
            st.session_state["custom_batch_rows"] = edited
            st.caption(f"{len(sweep_cases)} valid case(s) ready.")

        sweep_disabled = run_disabled or not sweep_cases
        if st.button(f"Run Sweep ({len(sweep_cases)} cases)",
                     disabled=sweep_disabled, type="primary", key="run_sweep_btn"):
            progress = st.progress(0.0, text="Starting sweep...")
            status_box = st.empty()

            def _cb(i, total, case):
                frac = i / max(total, 1)
                msg = (f"Case {i}/{total}: T={case.get('temp_c')}°C, "
                       f"LWC={case.get('lwc')}, MVD={case.get('mvd')}µm, "
                       f"alt={case.get('altitude_ft')}ft")
                progress.progress(min(frac, 1.0), text=msg)
                status_box.caption(msg)

            sweep_started = datetime.now()
            results, sweep_dir = _run_sweep(
                sweep_cases, airfoil_choice, designation, custom_points, uploaded_xyd,
                airfoil_label, chord, aoa, speed_ktas, output_root_dir,
                progress_cb=_cb,
            )
            elapsed = (datetime.now() - sweep_started).total_seconds()
            progress.progress(1.0, text=f"Sweep finished in {elapsed:.1f}s")

            if not results:
                st.error(f"Sweep failed before any case ran: {sweep_dir}")
            else:
                st.session_state["last_sweep_results"] = results
                st.session_state["last_sweep_dir"] = sweep_dir
                # Promote the worst-thickness successful case as the "latest run"
                # so the visualization and report sections pick it up.
                successful = [r for r in results if r["status"] == "success" and r["max_ice_mm"] is not None]
                if successful:
                    worst = max(successful, key=lambda r: r["max_ice_mm"])
                    worst_xyd = os.path.join(worst["output_dir"], "case.xyd")
                    st.session_state["last_run_dir"] = worst["output_dir"]
                    if os.path.isfile(worst_xyd):
                        st.session_state["last_run_xyd"] = worst_xyd
                    worst_inputs = {
                        "airfoil": airfoil_label,
                        "chord_m": round(float(chord), 6),
                        "aoa_deg": float(worst.get("AOA_deg", aoa)),
                        "speed_ktas": float(speed_ktas),
                        "altitude_ft": float(worst.get("altitude_ft", altitude_ft)),
                        "temp_c": float(worst.get("temp_C", temp_c)),
                        "lwc": float(worst.get("LWC_g_m3", lwc)),
                        "mvd": float(worst.get("MVD_um", mvd)),
                        "exposure_min": float(worst.get("exposure_min", exposure_min)),
                    }
                    st.session_state["last_run"] = {
                        "output_dir": worst["output_dir"],
                        "xyd_path": worst_xyd if os.path.isfile(worst_xyd) else None,
                        "inputs": worst_inputs,
                        "airfoil_label": airfoil_label,
                    }
                    _remember_run(worst["output_dir"], worst_xyd if os.path.isfile(worst_xyd) else None)
                    st.success(
                        f"Sweep complete. Worst case: #{worst['#']} ({worst['family']}, "
                        f"{worst['rationale']}) → {worst['max_ice_mm']:.1f} mm "
                        f"({worst['ice_type']}, {worst['risk']} risk). "
                        f"Visualization below now shows this case."
                    )
                else:
                    st.warning("Sweep finished but no successful cases produced ice geometry.")

        # Always show last sweep results if present
        last_results = st.session_state.get("last_sweep_results")
        if last_results:
            st.markdown("**Sweep results**")
            st.dataframe(last_results, width="stretch", hide_index=True)

            # CSV download
            import csv
            csv_buf = _io.StringIO()
            writer = csv.DictWriter(csv_buf, fieldnames=list(last_results[0].keys()))
            writer.writeheader()
            for row in last_results:
                writer.writerow(row)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            col_csv, col_zip = st.columns(2)
            col_csv.download_button(
                "\u2b07 Download summary (.csv)",
                data=csv_buf.getvalue(),
                file_name=f"lewice_sweep_{ts}.csv",
                mime="text/csv",
            )
            last_sweep_dir = st.session_state.get("last_sweep_dir")
            if last_sweep_dir and os.path.isdir(last_sweep_dir):
                zip_bytes = _zip_dir_to_bytes(last_sweep_dir)
                col_zip.download_button(
                    "\u2b07 Download all output files (.zip)",
                    data=zip_bytes,
                    file_name=f"lewice_sweep_{ts}.zip",
                    mime="application/zip",
                )

    st.divider()
    st.subheader("Ice Shape Visualization")

    # Latest run wins. Until then, show the shipped Example 1 result, labeled
    # with Example 1's conditions rather than whatever is currently in the sidebar.
    demo_xyd, demo_ice = _demo_sources()
    run_record = st.session_state.get("last_run")
    run_dir = None
    if run_record and os.path.isfile(os.path.join(run_record.get("output_dir", ""), "final1.dat")):
        run_dir = run_record["output_dir"]

    clean_plot = None
    ice_plot = None
    plot_title = ""
    shown_inputs = None
    shown_chord = chord
    shown_dir = None
    result_stale = False

    if run_dir:
        run_xyd = run_record.get("xyd_path")
        if run_xyd and os.path.isfile(run_xyd):
            clean_plot = parse_clean_airfoil(run_xyd)
        ice_plot = parse_ice_shape(os.path.join(run_dir, "final1.dat"))
        shown_inputs = run_record.get("inputs") or {}
        shown_chord = float(shown_inputs.get("chord_m", chord))
        shown_dir = run_dir
        plot_title = "LEWICE run — ice shape"
        result_stale = _inputs_differ(shown_inputs, sidebar_inputs)
        st.caption("Showing the latest LEWICE run: " + _format_conditions(shown_inputs))
        if result_stale:
            st.warning(
                "The sidebar has changed since this run. Thickness, ice type, and the "
                "shape below still belong to the completed run. Run again to update them."
            )
    elif demo_ice and os.path.isfile(demo_ice) and os.path.isfile(demo_xyd):
        clean_plot = parse_clean_airfoil(demo_xyd)
        ice_plot = parse_ice_shape(demo_ice)
        shown_inputs = DEMO_CASE["conditions"]
        shown_chord = DEMO_CASE["chord_m"]
        shown_dir = os.path.dirname(demo_ice)
        plot_title = "Example 1 — glaze, AOA 4.5°, −4.85 °C, 0.54 g/m³, 20 µm, 360 s"
        st.caption(
            "Showing NASA LEWICE distribution Example 1 (not the sidebar). "
            "Chord 0.9144 m, 90 m/s, 100000 Pa, TINF 268.30 K. Run a case to replace it."
        )
    else:
        if airfoil_choice == "Custom Point Array (2-D shape)" and custom_points:
            clean_plot = list(custom_points)
        elif airfoil_choice != "Upload Custom .xyd" and designation and airfoil_is_valid:
            try:
                clean_plot = naca4(designation, n_points=80)
            except ValueError as exc:
                st.warning(str(exc))
        plot_title = "Clean airfoil — no ice shape yet"
        st.caption("Run LEWICE to generate an ice shape. Example 1 output is not in this build.")

    case_metrics = {}
    if shown_dir and ice_plot:
        try:
            case_metrics = analyze_case(
                shown_dir,
                clean_plot,
                chord_m=shown_chord,
                temp_c=None if not shown_inputs else shown_inputs.get("temp_c"),
            )
        except Exception as exc:
            st.error(f"Could not read LEWICE outputs: {exc}")

    dark = dict(
        plot_bgcolor="#0B1A2E", paper_bgcolor="#0B1A2E",
        font=dict(color="#CCCCCC"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )

    fig2 = go.Figure()
    if clean_plot:
        fig2.add_trace(go.Scatter(
            x=[c[0] for c in clean_plot], y=[c[1] for c in clean_plot],
            mode="lines", name="Clean Airfoil",
            line=dict(color="#6699CC", width=1.5)
        ))
    if ice_plot:
        fig2.add_trace(go.Scatter(
            x=[c[0] for c in ice_plot], y=[c[1] for c in ice_plot],
            mode="lines", name="Iced Airfoil",
            line=dict(color="#C8A84E", width=2.5)
        ))
    frame_pts = list(clean_plot or []) + list(ice_plot or [])
    apply_equal_scale(fig2, frame_pts, uirevision=f"ice-{shown_dir}")
    fig2.update_layout(title=plot_title, **dark)
    st.plotly_chart(fig2, width="stretch", config={"scrollZoom": True})

    if ice_plot and shown_inputs:
        max_thick_display = case_metrics.get("max_thickness_mm")
        ice_type_run = _classify_ice(
            shown_inputs.get("temp_c", temp_c),
            shown_inputs.get("lwc", lwc),
            shown_inputs.get("mvd", mvd),
        )
        risk_run, _ = _assess_risk(max_thick_display or 0.0)
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric(
            "Max Ice Thickness",
            "n/a" if max_thick_display is None else f"{max_thick_display:.1f} mm",
        )
        mc2.metric("Screening ice type", ice_type_run)
        mc3.metric("Risk", risk_run)
        horn = case_metrics.get("horn_angle_deg")
        mc4.metric("Horn angle", "n/a" if horn is None else f"{horn:.0f}°")
        st.caption(
            "Max thickness is LEWICE ditot (ice height / chord) times the run chord, "
            "when thick.dat is present. Horn angle is the direction from the clean "
            "leading edge to the outermost nose point, measured from the chord-forward "
            "axis (positive toward the upper surface). Screening ice type is a "
            "temperature/LWC estimate, not the LEWICE freezing fraction."
        )
        if case_metrics.get("thickness_source"):
            st.caption(f"Thickness source: {case_metrics['thickness_source']}.")
        beta_max = case_metrics.get("beta_max")
        imp = case_metrics.get("impingement")
        c1, c2, c3 = st.columns(3)
        if beta_max is not None:
            c1.metric("Beta max", f"{beta_max:.3f}")
            c1.caption(
                f"at s/c = {case_metrics.get('beta_max_s'):.3f}"
                if case_metrics.get("beta_max_s") is not None else ""
            )
        if imp and imp.get("upper"):
            c2.metric("Upper limit x/c", f"{imp['upper']['x']:.3f}")
            c2.caption(f"final step, s/c = {imp['upper']['s']:.3f}")
        if imp and imp.get("lower"):
            c3.metric("Lower limit x/c", f"{imp['lower']['x']:.3f}")
            c3.caption(f"final step, s/c = {imp['lower']['s']:.3f}")
        for note in case_metrics.get("warnings") or []:
            st.warning(note)

    if ice_plot and clean_plot:
        st.subheader("Leading Edge Detail")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=[c[0] for c in clean_plot], y=[c[1] for c in clean_plot],
            mode="lines", name="Clean", line=dict(color="#6699CC", width=1.5)
        ))
        fig3.add_trace(go.Scatter(
            x=[c[0] for c in ice_plot], y=[c[1] for c in ice_plot],
            mode="lines", name="Iced", line=dict(color="#C8A84E", width=2.5),
            fill="toself", fillcolor="rgba(200,168,78,0.15)"
        ))
        le_pts = leading_edge_points(clean_plot, ice_plot)
        apply_equal_scale(fig3, le_pts, uirevision=f"le-{shown_dir}")
        fig3.update_layout(title="Leading edge — equal scale", **dark)
        st.plotly_chart(fig3, width="stretch", config={"scrollZoom": True})

    if shown_dir:
        beta_path = os.path.join(shown_dir, "beta.dat")
        htc_path = os.path.join(shown_dir, "htc.dat")
        if os.path.isfile(beta_path):
            beta_blocks = parse_beta(beta_path)
            if beta_blocks:
                block = beta_blocks[-1]
                fig_b = go.Figure()
                fig_b.add_trace(go.Scatter(
                    x=[r["s"] for r in block],
                    y=[r["beta"] for r in block],
                    mode="lines", name="beta",
                    line=dict(color="#7FDBFF", width=2),
                ))
                fig_b.update_layout(
                    title="Collection efficiency (final icing step)",
                    xaxis_title="s/c", yaxis_title="beta",
                    height=340, **dark,
                )
                st.plotly_chart(fig_b, width="stretch")
        if os.path.isfile(htc_path):
            htc_blocks = parse_htc(htc_path)
            if htc_blocks:
                block = htc_blocks[-1]
                fig_h = go.Figure()
                fig_h.add_trace(go.Scatter(
                    x=[r["s"] for r in block],
                    y=[r["htc"] for r in block],
                    mode="lines", name="htc",
                    line=dict(color="#C8A84E", width=2),
                ))
                fig_h.update_layout(
                    title="Heat transfer coefficient (final icing step)",
                    xaxis_title="s/c", yaxis_title="htc",
                    height=340, **dark,
                )
                st.plotly_chart(fig_h, width="stretch")

# ---- Tab 4: Report ----
with tab4:
    st.subheader("Certification Report Generator")
    st.markdown("Generate a professional, FAA-style PowerPoint report with ice shapes, "
                "conditions, impingement limits, risk assessment, and recommendations.")
    st.divider()

    # Report configuration
    rcol1, rcol2 = st.columns(2)
    with rcol1:
        project_name = st.text_input("Project / Aircraft Name", value="Aircraft Icing Analysis")
        analyst_name = st.text_input("Analyst Name", value="")
    with rcol2:
        report_notes = st.text_area("Additional Notes", value="", height=100)

    st.divider()

    # Risk bands are thickness only. Ice type is a separate screening estimate.
    ice_type_preview = _classify_ice(temp_c, lwc, mvd)
    st.markdown(
        f"**Screening ice type (sidebar):** `{ice_type_preview}`  |  "
        f"**Temp:** {temp_c} C  |  **LWC:** {lwc} g/m3  |  **MVD:** {mvd} um"
    )
    st.caption(
        "The screening type is a temperature and LWC estimate. It is not the freezing "
        "fraction from LEWICE. Risk bands below use thickness only."
    )

    risk_col1, risk_col2, risk_col3 = st.columns(3)
    with risk_col1:
        st.markdown('<div class="risk-green">LOW RISK</div>', unsafe_allow_html=True)
        st.caption("Thickness under 5 mm")
    with risk_col2:
        st.markdown('<div class="risk-yellow">MEDIUM RISK</div>', unsafe_allow_html=True)
        st.caption("Thickness 5–15 mm")
    with risk_col3:
        st.markdown('<div class="risk-red">HIGH RISK</div>', unsafe_allow_html=True)
        st.caption("Thickness over 15 mm")

    st.divider()

    output_sources = _collect_output_sources()
    demo_xyd, demo_ice = _demo_sources()

    st.markdown("**Choose report data source**")
    data_source = st.radio(
        "Ice Shape Data Source",
        [
            "Latest LEWICE run",
            "Pick from detected outputs",
            "Demo Case",
            "Manual folder path",
        ],
    )

    selected_source = None
    manual_output_dir = ""

    if data_source == "Latest LEWICE run":
        last = st.session_state.get("last_run")
        if last and os.path.isfile(os.path.join(last.get("output_dir", ""), "final1.dat")):
            selected_source = {
                "label": "Latest LEWICE run",
                "output_dir": last["output_dir"],
                "final_path": os.path.join(last["output_dir"], "final1.dat"),
                "xyd_path": last.get("xyd_path"),
                "inputs": last.get("inputs"),
                "airfoil_label": last.get("airfoil_label"),
            }
            st.info("Using the latest run: " + _format_conditions(last.get("inputs")))
        else:
            st.warning("No LEWICE run found yet. Run a case first or pick another source option.")
    elif data_source == "Pick from detected outputs":
        if output_sources:
            labels = [s["label"] for s in output_sources]
            choice = st.selectbox("Detected output folders", labels)
            selected_source = output_sources[labels.index(choice)]
            st.caption(selected_source["output_dir"])
        else:
            st.warning("No output folders with final1.dat were detected.")
    elif data_source == "Demo Case":
        if demo_ice and os.path.isfile(demo_xyd):
            selected_source = {
                "label": "Demo Case",
                "output_dir": os.path.dirname(demo_ice),
                "final_path": demo_ice,
                "xyd_path": demo_xyd,
                "inputs": DEMO_CASE["conditions"],
                "airfoil_label": DEMO_CASE["airfoil_name"],
                "chord_m": DEMO_CASE["chord_m"],
            }
            st.info(
                "Using LEWICE Example 1 (chord 0.9144 m, 90 m/s, −4.85 °C, "
                "0.54 g/m³, 20 µm, 360 s, 100000 Pa). Sidebar values are not substituted."
            )
        else:
            st.warning("Demo files are missing in this build. Use latest run or detected outputs.")
    else:
        manual_output_dir = st.text_input("Path to LEWICE output directory (containing final1.dat)", value="")
        st.caption("Tip: You usually do not need this. Prefer Latest LEWICE run.")

    report_format = st.radio("Report Format", ["PPTX", "PDF"], horizontal=True)

    if st.button(f"Export Certification Report (.{report_format.lower()})", type="primary"):
        with st.spinner("Generating certification report..."):
            clean_coords = None
            ice_coords = None
            max_thickness_mm = 0.0
            impingement = None

            if data_source == "Manual folder path":
                if manual_output_dir and os.path.isdir(manual_output_dir):
                    final_path = os.path.join(manual_output_dir, "final1.dat")
                    if os.path.isfile(final_path):
                        selected_source = {
                            "label": "Manual folder",
                            "output_dir": manual_output_dir,
                            "final_path": final_path,
                            "xyd_path": None,
                        }
                    else:
                        st.error(f"final1.dat not found in {manual_output_dir}")
                        st.stop()
                else:
                    st.error("Provide a valid output directory path.")
                    st.stop()

            if selected_source is None:
                st.error("No valid data source selected for report export.")
                st.stop()

            if selected_source.get("xyd_path") and os.path.isfile(selected_source["xyd_path"]):
                clean_coords = parse_clean_airfoil(selected_source["xyd_path"])

            ice_coords = parse_ice_shape(selected_source["final_path"])
            if not ice_coords:
                st.error("The ice-shape file has no coordinates.")
                st.stop()

            report_inputs = selected_source.get("inputs") or {
                "speed_ktas": speed_ktas,
                "altitude_ft": altitude_ft,
                "temp_c": temp_c,
                "lwc": lwc,
                "mvd": mvd,
                "exposure_min": exposure_min,
                "aoa_deg": aoa,
            }
            report_chord = float(selected_source.get("chord_m") or report_inputs.get("chord_m") or chord)
            report_airfoil = selected_source.get("airfoil_label") or airfoil_label
            if selected_source.get("inputs") is None and data_source != "Demo Case":
                st.warning(
                    "This folder has no saved flight conditions. The report uses the "
                    "current sidebar values, which may not be the conditions that produced the shape."
                )

            if clean_coords is None and airfoil_choice != "Upload Custom .xyd" and designation and airfoil_is_valid:
                try:
                    clean_coords = naca4(designation, n_points=80)
                except ValueError:
                    clean_coords = None

            metrics = analyze_case(
                selected_source["output_dir"],
                clean_coords,
                chord_m=report_chord,
                temp_c=report_inputs.get("temp_c"),
            )
            max_thickness_mm = metrics.get("max_thickness_mm") or 0.0
            impingement = metrics.get("impingement")

            report_kwargs = {
                "project_name": project_name,
                "airfoil_name": report_airfoil,
                "chord_m": report_chord,
                "conditions": report_inputs,
                "clean_coords": clean_coords,
                "ice_coords": ice_coords,
                "impingement_data": impingement,
                "max_thickness_mm": max_thickness_mm,
                "analyst_name": analyst_name,
                "notes": report_notes,
            }

            if report_format == "PDF":
                report_buf = build_pdf_report(**report_kwargs)
                report_ext = "pdf"
                report_mime = "application/pdf"
            else:
                report_buf = build_report(**report_kwargs)
                report_ext = "pptx"
                report_mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

            risk_level, _risk_desc = _assess_risk(max_thickness_mm)
            report_type = _classify_ice(
                report_inputs.get("temp_c", temp_c),
                report_inputs.get("lwc", lwc),
                report_inputs.get("mvd", mvd),
            )
            st.session_state["report_bytes"] = report_buf.getvalue() if hasattr(report_buf, "getvalue") else report_buf
            st.session_state["report_name"] = (
                f"LEWICE_Report_{project_name.replace(' ', '_')}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.{report_ext}"
            )
            st.session_state["report_mime"] = report_mime
            st.session_state["report_summary"] = (
                f"Report generated. Max thickness: {max_thickness_mm:.1f} mm | "
                f"Screening ice type: {report_type} | Risk: {risk_level}"
            )

    if st.session_state.get("report_bytes"):
        st.success(st.session_state.get("report_summary", "Report ready."))
        st.download_button(
            label="Download report",
            data=st.session_state["report_bytes"],
            file_name=st.session_state.get("report_name", "LEWICE_Report.pptx"),
            mime=st.session_state.get("report_mime", "application/octet-stream"),
            type="primary",
            key="download_report",
        )
