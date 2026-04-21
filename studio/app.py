"""
LEWICE Studio — Streamlit App
Modern UI for NASA LEWICE aircraft icing simulation.
No PhD in ice required.
"""
import re
import streamlit as st
import plotly.graph_objects as go
import json
import os
import sys
import tempfile
from datetime import datetime

# Add studio to path
sys.path.insert(0, os.path.dirname(__file__))

from lewice_engine.input_builder import (
    build_case_from_friendly, build_input, write_input,
    celsius_to_kelvin, ktas_to_ms, altitude_to_pressure, DEFAULTS
)
from lewice_engine.output_parser import parse_clean_airfoil, parse_ice_shape, compute_ice_metrics
from airfoils.naca_library import naca4, write_xyd, COMMON_AIRFOILS
from reports.generator import build_report, _classify_ice, _assess_risk

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

APP_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(APP_DIR, ".."))


def _demo_sources():
    demo_xyd = os.path.join(REPO_ROOT, "Inputs", "case1.xyd")
    demo_ice_candidates = [
        os.path.join(APP_DIR, "test_run", "case1", "final1.dat"),
        os.path.join(REPO_ROOT, "results", "case22", "final1.dat"),
    ]

    demo_ice = None
    for candidate in demo_ice_candidates:
        if os.path.isfile(candidate):
            demo_ice = candidate
            break

    return demo_xyd, demo_ice


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
    "Airfoil",
    list(COMMON_AIRFOILS.keys()) + ["Custom NACA Code", "Upload Custom .xyd"],
)

designation = None
airfoil_label = airfoil_choice
airfoil_is_valid = True

if airfoil_choice in COMMON_AIRFOILS:
    designation = COMMON_AIRFOILS[airfoil_choice]
elif airfoil_choice == "Custom NACA Code":
    custom_naca = st.sidebar.text_input("NACA Code", value="23012", help="Examples: 2412, 4415, 23012")
    candidate = custom_naca.strip().upper().replace("NACA", "").replace("-", "").replace(" ", "")
    if re.fullmatch(r"\d{4}|\d{5}", candidate):
        designation = candidate
        airfoil_label = f"NACA {designation}"
        if len(designation) == 5:
            st.sidebar.caption("5-digit NACA camber line is approximate in this generator; thickness is exact.")
    else:
        airfoil_is_valid = False
        st.sidebar.error("Enter a valid NACA code: 4 digits (e.g. 2412) or 5 digits (e.g. 23012).")

if designation:
    airfoil_label = f"NACA {designation}"

if airfoil_choice == "Upload Custom .xyd":
    uploaded_xyd = st.sidebar.file_uploader("Upload .xyd file", type=["xyd", "dat", "txt"])
else:
    uploaded_xyd = None

chord = st.sidebar.number_input("Chord Length (m)", value=0.9144, min_value=0.01, max_value=50.0, step=0.01)
aoa = st.sidebar.number_input("Angle of Attack (deg)", value=0.0, min_value=-15.0, max_value=25.0, step=0.5)

st.sidebar.header("Flight Conditions")
speed_ktas = st.sidebar.number_input("Speed (KTAS)", value=175.0, min_value=50.0, max_value=600.0, step=5.0)
altitude_ft = st.sidebar.number_input("Altitude (ft)", value=10000, min_value=0, max_value=45000, step=500)
temp_c = st.sidebar.number_input("Temperature (C)", value=-10.0, min_value=-40.0, max_value=0.0, step=1.0)

st.sidebar.header("Icing Conditions")

envelope_mode = st.sidebar.radio("Mode", ["Single Condition", "Appendix C Envelope", "Custom Batch"])

MODE_HELP = {
    "Single Condition": "Run one LEWICE case using the exact LWC, MVD, and exposure values set below.",
    "Appendix C Envelope": "Preview and run against the FAA Appendix C standard condition set for certification-style sweeps.",
    "Custom Batch": "Run multiple user-defined cases as a batch. Right now this is a planning mode label; batch execution UI is not wired in this page yet.",
}
st.sidebar.caption(MODE_HELP[envelope_mode])

lwc = st.sidebar.number_input("LWC (g/m3)", value=0.54, min_value=0.05, max_value=3.0, step=0.05)
mvd = st.sidebar.number_input("MVD (microns)", value=20.0, min_value=5.0, max_value=50.0, step=1.0)
exposure_min = st.sidebar.number_input("Exposure Time (min)", value=6.0, min_value=0.5, max_value=45.0, step=0.5)

# ---------- Main Panel ----------
tab1, tab2, tab3, tab4 = st.tabs(["Airfoil Preview", "LEWICE Input", "Run & Results", "Report"])

# ---- Tab 1: Airfoil Preview ----
with tab1:
    st.subheader("Airfoil Geometry")

    if airfoil_choice != "Upload Custom .xyd" and designation and airfoil_is_valid:
        coords = naca4(designation, n_points=80)
        x_vals = [c[0] for c in coords]
        y_vals = [c[1] for c in coords]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Clean Airfoil",
                                 line=dict(color="#1a73e8", width=2)))
        fig.update_layout(
            xaxis_title="x/c", yaxis_title="y/c",
            yaxis=dict(scaleanchor="x", scaleratio=1),
            height=400, margin=dict(l=40, r=40, t=30, b=40),
            title=f"{airfoil_label} — {len(coords)} points"
        )
        st.plotly_chart(fig, width="stretch")

        col1, col2, col3 = st.columns(3)
        col1.metric("Points", len(coords))
        col2.metric("Max Thickness", f"{int(designation[-2:])}%")
        if len(designation) == 4:
            col3.metric("Max Camber", f"{int(designation[0])}%")
        else:
            col3.metric("Series", "5-digit")
    else:
        if uploaded_xyd:
            content = uploaded_xyd.read().decode("utf-8")
            coords = []
            for line in content.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        coords.append((float(parts[0]), float(parts[1])))
                    except ValueError:
                        pass
            x_vals = [c[0] for c in coords]
            y_vals = [c[1] for c in coords]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines",
                                     line=dict(color="#1a73e8", width=2)))
            fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), height=400)
            st.plotly_chart(fig, width="stretch")
            st.metric("Points", len(coords))
        else:
            st.info("Upload a .xyd file to preview the airfoil geometry.")
    if airfoil_choice != "Upload Custom .xyd" and (not designation or not airfoil_is_valid):
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

    if envelope_mode == "Appendix C Envelope":
        env_path = os.path.join(os.path.dirname(__file__), "envelopes", "appendix_c.json")
        if os.path.isfile(env_path):
            with open(env_path, encoding="utf-8-sig") as f:
                envelope = json.load(f)
            st.info(f"Appendix C envelope loaded: {len(envelope['conditions'])} continuous + {len(envelope['intermittent_maximum'])} intermittent conditions")
            st.json(envelope["conditions"][:5])
            st.caption("Showing first 5 of " + str(len(envelope["conditions"])) + " conditions...")

# ---- Tab 3: Run & Results ----
with tab3:
    st.subheader("Run LEWICE")

    lewice_exe = os.path.join(os.path.dirname(__file__), "..", "lewice.exe")
    exe_exists = os.path.isfile(os.path.abspath(lewice_exe))

    if exe_exists:
        st.success(f"LEWICE executable found: lewice.exe")
    else:
        st.error(f"LEWICE executable not found at expected path. Place lewice.exe in the LEWICE root directory.")

    run_disabled = (not exe_exists) or (airfoil_choice != "Upload Custom .xyd" and (not designation or not airfoil_is_valid))
    if st.button("Run Single Case", disabled=run_disabled, type="primary"):
        st.info("Running LEWICE... this typically takes 5-30 seconds per case.")
        with st.spinner("Simulating ice accretion..."):
            tmp_dir = tempfile.mkdtemp(prefix="lewice_studio_")
            inp_path = os.path.join(tmp_dir, "case.inp")
            xyd_path = os.path.join(tmp_dir, "case.xyd")

            write_input(inp_path, params, title=f"Studio Run - {airfoil_label}")

            if airfoil_choice != "Upload Custom .xyd":
                foil_coords = naca4(designation, n_points=80)
                write_xyd(xyd_path, foil_coords)
            elif uploaded_xyd:
                content = uploaded_xyd.getvalue().decode("utf-8")
                with open(xyd_path, "w") as f:
                    f.write(content)
            else:
                st.error("Upload a valid .xyd file before running LEWICE.")
                st.stop()

            from lewice_engine.runner import run_lewice
            result = run_lewice(inp_path, xyd_path, work_dir=tmp_dir)

            if result["status"] == "success":
                st.success(f"LEWICE completed in {result['elapsed_seconds']}s")
                st.session_state["last_run_dir"] = tmp_dir
                st.session_state["last_run_xyd"] = xyd_path
                _remember_run(tmp_dir, xyd_path)
            else:
                st.error(f"LEWICE failed: {result.get('message', result.get('stderr', 'Unknown error'))}")

    st.divider()
    st.subheader("Ice Shape Visualization")

    # Determine which data to show: last run > demo case 1 > clean only
    demo_xyd, demo_ice = _demo_sources()
    run_dir = st.session_state.get("last_run_dir", None)

    clean_plot = None
    ice_plot = None
    plot_title = ""
    max_thick_display = 0.0

    if run_dir and os.path.isfile(os.path.join(run_dir, "final1.dat")):
        # Show results from latest run
        run_xyd = st.session_state.get("last_run_xyd", None)
        if run_xyd and os.path.isfile(run_xyd):
            clean_plot = parse_clean_airfoil(run_xyd)
        ice_plot = parse_ice_shape(os.path.join(run_dir, "final1.dat"))
        plot_title = "LEWICE Run Result — Ice Shape Overlay"
        st.caption("Showing results from latest LEWICE run.")
    elif demo_ice and os.path.isfile(demo_ice) and os.path.isfile(demo_xyd):
        # Show demo Case 1 data
        clean_plot = parse_clean_airfoil(demo_xyd)
        ice_plot = parse_ice_shape(demo_ice)
        plot_title = "Demo — NASA Case 1 Validation (AOA 4.5, -4.85C, 0.54 g/m3, 20um)"
        st.caption("Showing NASA LEWICE Case 1 validation data. Run your own case to replace.")
    else:
        # No ice data available — show clean airfoil only
        if airfoil_choice != "Upload Custom .xyd" and designation and airfoil_is_valid:
            clean_plot = naca4(designation, n_points=80)
        plot_title = "Clean Airfoil (no ice data yet — run LEWICE or add demo data)"
        st.caption("Run LEWICE to generate ice shape data.")

    # Build the plot
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
        min_x_ice = min(c[0] for c in ice_plot)
        max_thick_display = abs(min_x_ice) * chord * 1000

    fig2.update_layout(
        xaxis_title="x/c", yaxis_title="y/c",
        yaxis=dict(scaleanchor="x", scaleratio=1),
        height=450, title=plot_title,
        plot_bgcolor="#0B1A2E", paper_bgcolor="#0B1A2E",
        font=dict(color="#CCCCCC"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig2, width="stretch")

    # Metrics row
    if ice_plot:
        mc1, mc2, mc3, mc4 = st.columns(4)
        ice_type_run = _classify_ice(temp_c, lwc, mvd)
        risk_run, _ = _assess_risk(max_thick_display)
        mc1.metric("Max Ice Thickness", f"{max_thick_display:.1f} mm")
        mc2.metric("Ice Type", ice_type_run)
        mc3.metric("Risk", risk_run)
        mc4.metric("Ice Points", len(ice_plot))

    # LE detail zoom
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
            fill="toself", fillcolor="rgba(200,168,78,0.1)"
        ))
        fig3.update_layout(
            xaxis=dict(range=[-0.08, 0.30]), yaxis=dict(range=[-0.12, 0.12], scaleanchor="x"),
            height=400, title="Leading Edge — Ice Accretion Detail",
            plot_bgcolor="#0B1A2E", paper_bgcolor="#0B1A2E",
            font=dict(color="#CCCCCC"), legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig3, width="stretch")

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

    # Risk preview
    ice_type_preview = _classify_ice(temp_c, lwc, mvd)
    st.markdown(f"**Predicted Ice Type:** `{ice_type_preview}`  |  "
                f"**Temp:** {temp_c} C  |  **LWC:** {lwc} g/m3  |  **MVD:** {mvd} um")

    risk_col1, risk_col2, risk_col3 = st.columns(3)
    with risk_col1:
        st.markdown('<div class="risk-green">LOW RISK</div>', unsafe_allow_html=True)
        st.caption("Rime ice, < 5 mm thickness")
    with risk_col2:
        st.markdown('<div class="risk-yellow">MEDIUM RISK</div>', unsafe_allow_html=True)
        st.caption("Mixed ice, 5-15 mm thickness")
    with risk_col3:
        st.markdown('<div class="risk-red">HIGH RISK</div>', unsafe_allow_html=True)
        st.caption("Glaze ice, > 15 mm, horn formations")

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
        if output_sources:
            selected_source = output_sources[0]
            st.info(f"Using: {selected_source['output_dir']}")
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
            }
            st.info(f"Using demo data from: {selected_source['output_dir']}")
        else:
            st.warning("Demo files are missing in this build. Use latest run or detected outputs.")
    else:
        manual_output_dir = st.text_input("Path to LEWICE output directory (containing final1.dat)", value="")
        st.caption("Tip: You usually do not need this. Prefer Latest LEWICE run.")

    if st.button("Export Certification Report (.pptx)", type="primary"):
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
            min_x = min(c[0] for c in ice_coords)
            max_thickness_mm = abs(min_x) * chord * 1000

            if data_source == "Demo Case":
                impingement = {
                    "upper": {"x": 0.003625, "y": 0.005619, "s": 0.020414},
                    "lower": {"x": 0.145164, "y": -0.030770, "s": -0.143421},
                }

            if clean_coords is None and airfoil_choice != "Upload Custom .xyd" and designation and airfoil_is_valid:
                clean_coords = naca4(designation, n_points=80)

            report_buf = build_report(
                project_name=project_name,
                airfoil_name=airfoil_label,
                chord_m=chord,
                conditions={
                    "speed_ktas": speed_ktas,
                    "altitude_ft": altitude_ft,
                    "temp_c": temp_c,
                    "lwc": lwc,
                    "mvd": mvd,
                    "exposure_min": exposure_min,
                    "aoa_deg": aoa,
                },
                clean_coords=clean_coords,
                ice_coords=ice_coords,
                impingement_data=impingement,
                max_thickness_mm=max_thickness_mm,
                analyst_name=analyst_name,
                notes=report_notes,
            )

            risk_level, risk_desc = _assess_risk(max_thickness_mm)
            st.success(f"Report generated!  Max thickness: {max_thickness_mm:.1f} mm  |  "
                       f"Ice type: {ice_type_preview}  |  Risk: {risk_level}")

            st.download_button(
                label="Download Report (.pptx)",
                data=report_buf,
                file_name=f"LEWICE_Report_{project_name.replace(' ', '_')}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                type="primary",
            )
