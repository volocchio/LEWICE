"""
LEWICE Studio — Streamlit App
Modern UI for NASA LEWICE aircraft icing simulation.
No PhD in ice required.
"""
import streamlit as st
import plotly.graph_objects as go
import json
import os
import sys
import tempfile

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

# ---------- Sidebar: Configuration ----------
st.sidebar.header("Aircraft & Flight Conditions")

# Airfoil selection
airfoil_choice = st.sidebar.selectbox("Airfoil", list(COMMON_AIRFOILS.keys()) + ["Upload Custom .xyd"])
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

lwc = st.sidebar.number_input("LWC (g/m3)", value=0.54, min_value=0.05, max_value=3.0, step=0.05)
mvd = st.sidebar.number_input("MVD (microns)", value=20.0, min_value=5.0, max_value=50.0, step=1.0)
exposure_min = st.sidebar.number_input("Exposure Time (min)", value=6.0, min_value=0.5, max_value=45.0, step=0.5)

# ---------- Main Panel ----------
tab1, tab2, tab3, tab4 = st.tabs(["Airfoil Preview", "LEWICE Input", "Run & Results", "Report"])

# ---- Tab 1: Airfoil Preview ----
with tab1:
    st.subheader("Airfoil Geometry")

    if airfoil_choice != "Upload Custom .xyd":
        designation = COMMON_AIRFOILS[airfoil_choice]
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
            title=f"{airfoil_choice} — {len(coords)} points"
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Points", len(coords))
        col2.metric("Max Thickness", f"{int(designation[2:4])}%")
        col3.metric("Max Camber", f"{int(designation[0])}%")
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
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Points", len(coords))
        else:
            st.info("Upload a .xyd file to preview the airfoil geometry.")

# ---- Tab 2: LEWICE Input Preview ----
with tab2:
    st.subheader("Generated LEWICE Input File")

    params = build_case_from_friendly(
        chord_m=chord, aoa_deg=aoa,
        speed_ktas=speed_ktas, altitude_ft=altitude_ft,
        temp_c=temp_c, lwc=lwc, mvd=mvd,
        exposure_min=exposure_min,
    )
    inp_text = build_input(params, title=f"LEWICE Studio - {airfoil_choice}")
    st.code(inp_text, language="fortran")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocity (m/s)", f"{params['VINF']:.1f}")
    col2.metric("Temperature (K)", f"{params['TINF']:.1f}")
    col3.metric("Pressure (Pa)", f"{params['PINF']:.0f}")
    col4.metric("Exposure (s)", f"{params['TSTOP']:.0f}")

    if envelope_mode == "Appendix C Envelope":
        env_path = os.path.join(os.path.dirname(__file__), "envelopes", "appendix_c.json")
        if os.path.isfile(env_path):
            with open(env_path) as f:
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

    if st.button("Run Single Case", disabled=not exe_exists, type="primary"):
        st.info("Running LEWICE... this typically takes 5-30 seconds per case.")
        with st.spinner("Simulating ice accretion..."):
            # Write temp input and geometry files
            tmp_dir = tempfile.mkdtemp(prefix="lewice_studio_")
            inp_path = os.path.join(tmp_dir, "case.inp")
            xyd_path = os.path.join(tmp_dir, "case.xyd")

            write_input(inp_path, params, title=f"Studio Run - {airfoil_choice}")

            if airfoil_choice != "Upload Custom .xyd":
                designation = COMMON_AIRFOILS[airfoil_choice]
                foil_coords = naca4(designation, n_points=80)
                write_xyd(xyd_path, foil_coords)
            elif uploaded_xyd:
                with open(xyd_path, "w") as f:
                    f.write(content)

            from lewice_engine.runner import run_lewice
            result = run_lewice(inp_path, xyd_path, work_dir=tmp_dir)

            if result["status"] == "success":
                st.success(f"LEWICE completed in {result['elapsed_seconds']}s")
                st.text(result.get("stdout", "")[:2000])
            else:
                st.error(f"LEWICE failed: {result.get('message', result.get('stderr', 'Unknown error'))}")

    st.divider()
    st.subheader("Ice Shape Visualization (Demo)")
    st.caption("After running LEWICE, ice shapes will be plotted here overlaid on the clean airfoil.")

    # Demo placeholder with clean airfoil
    if airfoil_choice != "Upload Custom .xyd":
        designation = COMMON_AIRFOILS[airfoil_choice]
        clean = naca4(designation, n_points=80)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=[c[0] for c in clean], y=[c[1] for c in clean],
            mode="lines", name="Clean Airfoil", line=dict(color="#1a73e8", width=2)
        ))
        fig2.update_layout(
            xaxis_title="x/c", yaxis_title="y/c",
            yaxis=dict(scaleanchor="x", scaleratio=1),
            height=400, title="Ice Shape Overlay (run LEWICE to populate)"
        )
        st.plotly_chart(fig2, use_container_width=True)

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

    # Data source
    data_source = st.radio("Ice Shape Data Source", [
        "Use demo Case 1 data (NASA validation)",
        "Load from LEWICE output folder",
    ])

    ice_output_dir = None
    if data_source == "Load from LEWICE output folder":
        ice_output_dir = st.text_input(
            "Path to LEWICE output directory (containing final1.dat)", value="")

    if st.button("Export Certification Report (.pptx)", type="primary"):
        with st.spinner("Generating certification report..."):
            clean_coords = None
            ice_coords = None
            max_thickness_mm = 0.0
            impingement = None

            if data_source == "Use demo Case 1 data (NASA validation)":
                demo_xyd = os.path.join(os.path.dirname(__file__), "..", "Inputs", "case1.xyd")
                demo_ice = os.path.join(os.path.dirname(__file__), "test_run", "case1", "final1.dat")

                if os.path.isfile(demo_xyd) and os.path.isfile(demo_ice):
                    clean_coords = parse_clean_airfoil(demo_xyd)
                    ice_coords = parse_ice_shape(demo_ice)
                    min_x = min(c[0] for c in ice_coords)
                    max_thickness_mm = abs(min_x) * chord * 1000
                    impingement = {
                        "upper": {"x": 0.003625, "y": 0.005619, "s": 0.020414},
                        "lower": {"x": 0.145164, "y": -0.030770, "s": -0.143421},
                    }
                else:
                    st.error("Demo data not found. Run LEWICE Case 1 first.")
                    st.stop()
            else:
                if ice_output_dir and os.path.isdir(ice_output_dir):
                    final_path = os.path.join(ice_output_dir, "final1.dat")
                    if os.path.isfile(final_path):
                        ice_coords = parse_ice_shape(final_path)
                        min_x = min(c[0] for c in ice_coords)
                        max_thickness_mm = abs(min_x) * chord * 1000
                    else:
                        st.error(f"final1.dat not found in {ice_output_dir}")
                        st.stop()
                else:
                    st.error("Provide a valid output directory path.")
                    st.stop()

            if clean_coords is None and airfoil_choice != "Upload Custom .xyd":
                designation = COMMON_AIRFOILS[airfoil_choice]
                clean_coords = naca4(designation, n_points=80)

            report_buf = build_report(
                project_name=project_name,
                airfoil_name=airfoil_choice,
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
