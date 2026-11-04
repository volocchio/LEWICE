"""Tests for the LEWICE Studio fixes.

Run from the repository root:

    python -m unittest studio.tests.test_lewice_studio

The integration test runs lewice.exe through Wine when both are available
and skips otherwise.
"""
import math
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from airfoils.naca_library import naca4, naca_camber_kind, _camber_5
from lewice_engine.input_builder import (
    altitude_to_pressure,
    build_case_from_friendly,
    build_input,
    celsius_to_kelvin,
    fahrenheit_to_kelvin,
    icing_steps,
    ktas_to_ms,
)
from lewice_engine.output_parser import (
    analyze_case,
    parse_beta,
    parse_clean_airfoil,
    parse_reported_thickness,
    parse_xy_text,
)
from lewice_engine.plots import apply_equal_scale, bounds, configure_equal_axes
from lewice_engine.runner import probe_lewice, run_lewice

import plotly.graph_objects as go

STUDIO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXAMPLE = os.path.join(STUDIO, "examples", "case1")


class TestUnits(unittest.TestCase):
    def test_ktas_and_temperature(self):
        self.assertAlmostEqual(ktas_to_ms(1.0), 1852.0 / 3600.0, places=9)
        self.assertAlmostEqual(ktas_to_ms(175.0), 90.0278, places=3)
        self.assertAlmostEqual(celsius_to_kelvin(-10.0), 263.15, places=6)
        self.assertAlmostEqual(celsius_to_kelvin(-4.85), 268.30, places=2)
        self.assertAlmostEqual(fahrenheit_to_kelvin(32.0), 273.15, places=6)

    def test_isa_pressure_troposphere_and_stratosphere(self):
        self.assertAlmostEqual(altitude_to_pressure(0), 101325.0, delta=1.0)
        # Standard sea-level-to-10,000 ft pressure is about 69.7 kPa.
        self.assertAlmostEqual(altitude_to_pressure(10000), 69682.0, delta=80.0)
        # Continuous across the tropopause (36,089.24 ft).
        below = altitude_to_pressure(36089)
        above = altitude_to_pressure(36090)
        self.assertAlmostEqual(below, above, delta=5.0)
        # 45,000 ft is in the isothermal layer. The old lapse-only formula
        # keeps cooling and lands several hundred Pa low (about 14.5 kPa
        # instead of about 14.75 kPa).
        p_45 = altitude_to_pressure(45000)
        self.assertAlmostEqual(p_45, 14748.0, delta=40.0)
        self.assertGreater(p_45, 14700.0)

    def test_lewice_namelist_units_and_iflo(self):
        # 6 minutes -> 6 icing updates, matching distribution Example 1.
        params = build_case_from_friendly(
            chord_m=36.0 * 0.0254,
            aoa_deg=4.5,
            speed_ktas=90.0 / (1852.0 / 3600.0),
            pressure_pa=100000.0,
            temp_c=-4.85,
            lwc=0.54,
            mvd=20.0,
            exposure_min=6.0,
        )
        self.assertAlmostEqual(params["CHORD"], 0.9144, places=4)
        self.assertAlmostEqual(params["VINF"], 90.0, places=3)
        self.assertAlmostEqual(params["TINF"], 268.30, places=2)
        self.assertEqual(params["LWC"], 0.54)
        self.assertEqual(params["DPD"], 20.0)
        self.assertEqual(params["TSTOP"], 360.0)
        self.assertEqual(params["IFLO"], 6)
        self.assertEqual(params["NPL"], 24)
        text = build_input(params, title="Example & check")
        self.assertIn("LWC    = 0.540", text)
        self.assertIn("DPD    = 20.0", text)
        self.assertIn("DSMN   = 4.0D-4", text)
        self.assertNotIn("&", text.splitlines()[0])
        self.assertEqual(icing_steps(30.0), 1)
        self.assertEqual(icing_steps(420.0), 7)
        self.assertEqual(icing_steps(45.0 * 60.0), 24)


class TestAirfoils(unittest.TestCase):
    def test_thickness_extremes_and_closed_contour(self):
        for code, expected in (("0006", 0.06), ("0012", 0.12), ("0030", 0.30)):
            coords = naca4(code, n_points=80)
            self.assertEqual(coords[0], coords[-1])
            thickness = max(p[1] for p in coords) - min(p[1] for p in coords)
            self.assertAlmostEqual(thickness, expected, delta=0.004)
            self.assertAlmostEqual(min(p[0] for p in coords), 0.0, places=4)
            self.assertAlmostEqual(max(p[0] for p in coords), 1.0, delta=0.002)

    def test_four_digit_camber_unchanged(self):
        from airfoils.naca_library import _camber_4
        xs = [i / 400 for i in range(1, 400)]
        x_peak = max(xs, key=lambda x: _camber_4(x, 0.02, 0.4)[0])
        self.assertAlmostEqual(x_peak, 0.4, delta=0.01)
        self.assertAlmostEqual(_camber_4(0.4, 0.02, 0.4)[0], 0.02, places=4)

    def test_five_digit_23012_mean_line(self):
        self.assertEqual(naca_camber_kind("23012"), "5-digit")
        # Max camber of the 230 mean line is at 15% chord, not at the
        # 4-digit reading (2% camber at 30% chord).
        xs = [i / 200 for i in range(1, 200)]
        yc = [(x, _camber_5(x, 0.2025, 15.957, None)[0]) for x in xs]
        x_peak, y_peak = max(yc, key=lambda p: p[1])
        self.assertAlmostEqual(x_peak, 0.15, delta=0.01)
        self.assertAlmostEqual(y_peak, 0.0184, delta=0.001)
        with self.assertRaises(ValueError):
            naca4("26012")

    def test_point_text_accepts_commas(self):
        coords, errors = parse_xy_text("1.0, 0.0\n0, 0\n0.5, 0.1\n# comment\n")
        self.assertEqual(errors, [])
        self.assertEqual(len(coords), 3)
        self.assertEqual(coords[1], (0.0, 0.0))


class TestExample1Outputs(unittest.TestCase):
    def test_beta_columns_and_peak_near_nose(self):
        blocks = parse_beta(os.path.join(EXAMPLE, "beta.dat"))
        self.assertGreaterEqual(len(blocks), 1)
        peak = max(blocks[-1], key=lambda r: r["beta"])
        # The old parser stored sle/c in "x". sle at the peak is not the
        # geometric x (the peak sits just ahead of the leading edge).
        self.assertGreaterEqual(peak["beta"], 0.0)
        self.assertLessEqual(peak["beta"], 1.0)
        self.assertLess(abs(peak["s"]), 0.05)
        self.assertLess(peak["x"], 0.02)
        self.assertGreater(peak["x"], -0.05)
        betas = [r["beta"] for r in blocks[-1]]
        self.assertGreaterEqual(min(betas), 0.0)
        self.assertLessEqual(max(betas), 1.0)

    def test_thickness_horn_and_limits(self):
        clean = parse_clean_airfoil(os.path.join(EXAMPLE, "case.xyd"))
        metrics = analyze_case(EXAMPLE, clean, chord_m=0.9144, temp_c=-4.85)
        # LEWICE log: 0.01400 c. thick.dat ditot max is 0.01366 c.
        self.assertAlmostEqual(metrics["lewice_log_thickness_c"], 0.01400, delta=0.0002)
        self.assertAlmostEqual(metrics["max_thickness_c"], 0.01366, delta=0.0003)
        self.assertAlmostEqual(metrics["max_thickness_mm"], 12.49, delta=0.3)
        self.assertEqual(metrics["thickness_source"], "thick.dat ditot/c")
        # Glaze horn is forward and above the leading edge, not the foremost-x
        # proxy and not a point on the bare lower surface.
        self.assertLess(metrics["horn_x"], 0.0)
        self.assertGreater(metrics["horn_y"], 0.0)
        self.assertGreater(metrics["horn_angle_deg"], 30.0)
        self.assertLess(metrics["horn_angle_deg"], 90.0)
        upper = metrics["impingement"]["upper"]
        lower = metrics["impingement"]["lower"]
        self.assertGreater(upper["s"], lower["s"])
        self.assertLess(lower["y"], 0.0)
        self.assertEqual(metrics["warnings"], [])

    def test_log_thickness_uses_the_final_step(self):
        with open(os.path.join(EXAMPLE, "lewice_stdout.txt"), encoding="utf-8") as log_f:
            text = log_f.read()
        self.assertAlmostEqual(parse_reported_thickness(text), 0.0140024665, places=6)


class TestEqualScale(unittest.TestCase):
    def test_plotly_anchor_and_padding(self):
        pts = [(0.0, -0.06), (1.0, 0.0), (0.0, 0.06)]
        fig = go.Figure(go.Scatter(x=[p[0] for p in pts], y=[p[1] for p in pts]))
        apply_equal_scale(fig, pts, uirevision="airfoil")
        self.assertEqual(fig.layout.yaxis.scaleanchor, "x")
        self.assertEqual(fig.layout.yaxis.scaleratio, 1)
        self.assertEqual(fig.layout.yaxis.constrain, "domain")
        self.assertEqual(fig.layout.xaxis.constrain, "domain")
        self.assertEqual(fig.layout.uirevision, "airfoil")
        x0, x1 = fig.layout.xaxis.range
        y0, y1 = fig.layout.yaxis.range
        self.assertLess(x0, 0.0)
        self.assertGreater(x1, 1.0)
        self.assertLess(y0, -0.06)
        self.assertGreater(y1, 0.06)

    def test_matplotlib_pixels_match(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        ax.plot([0, 1, 0], [0, 0.05, 0])
        configure_equal_axes(ax, [(0, 0), (1, 0), (0, 0.12), (1, -0.06)])
        fig.canvas.draw()
        origin = ax.transData.transform((0, 0))
        right = ax.transData.transform((1, 0))
        up = ax.transData.transform((0, 1))
        dx = abs(right[0] - origin[0])
        dy = abs(up[1] - origin[1])
        self.assertAlmostEqual(dx, dy, delta=0.02 * dx)
        plt.close(fig)

    def test_padding_is_the_same_absolute_amount(self):
        xr, yr = bounds([(0, 0), (1, 0.1)])
        self.assertAlmostEqual((xr[1] - 1) - (0 - xr[0]), 0.0, places=9)
        self.assertAlmostEqual((xr[1] - 1), (yr[1] - 0.1), places=9)


class TestRunnerMessages(unittest.TestCase):
    def test_missing_executable_is_explicit(self):
        info = probe_lewice(exe_path="/tmp/does-not-exist-lewice.exe")
        self.assertFalse(info["ok"])
        self.assertIn("not found", info["message"].lower())

    def test_missing_wine_is_explicit(self):
        with mock.patch("lewice_engine.runner.shutil.which", return_value=None):
            info = probe_lewice(exe_path=os.path.join(STUDIO, "..", "lewice.exe"))
        if os.name == "nt":
            self.skipTest("Wine is not used on Windows")
        self.assertFalse(info["ok"])
        self.assertIn("Wine", info["message"])
        self.assertIn("lewice.exe", info["message"])

    def test_run_reports_missing_inputs(self):
        result = run_lewice("/tmp/no-such.inp", "/tmp/no-such.xyd", work_dir=tempfile.mkdtemp())
        self.assertEqual(result["status"], "error")
        self.assertTrue(result["message"])


class TestLewiceIntegration(unittest.TestCase):
    def test_generated_input_runs_and_beta_is_physical(self):
        info = probe_lewice()
        if not info["ok"]:
            self.skipTest(info["message"])
        work = tempfile.mkdtemp(prefix="lewice_test_")
        try:
            params = build_case_from_friendly(
                chord_m=0.5334,
                aoa_deg=3.5,
                speed_ms=102.8,
                pressure_pa=100000.0,
                temp_c=-22.78,
                lwc=0.55,
                mvd=20.0,
                exposure_min=2.0,
            )
            self.assertEqual(params["IFLO"], 2)
            inp = os.path.join(work, "case.inp")
            xyd = os.path.join(work, "case.xyd")
            with open(inp, "w") as f:
                f.write(build_input(params, "studio integration"))
            coords = naca4("0012", n_points=60)
            with open(xyd, "w") as f:
                for x, y in coords:
                    f.write(f"{x:.6f} {y:.6f}\n")
            result = run_lewice(inp, xyd, work_dir=work, timeout=180)
            self.assertEqual(result["status"], "success", result.get("message"))
            self.assertIn("final1.dat", os.listdir(work))
            metrics = analyze_case(work, coords, chord_m=0.5334, temp_c=-22.78, log_text=result.get("stdout"))
            self.assertIsNotNone(metrics["beta_max"])
            self.assertGreaterEqual(metrics["beta_min"], -0.01)
            self.assertLessEqual(metrics["beta_max"], 1.02)
            self.assertLess(abs(metrics["beta_max_s"]), 0.1)
            self.assertGreater(metrics["max_thickness_mm"], 0.0)
            self.assertLess(metrics["horn_x"], 0.1)
            self.assertIsNotNone(metrics["horn_angle_deg"])
        finally:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
