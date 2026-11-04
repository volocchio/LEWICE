"""
LEWICE Input Builder
Generates valid LEWICE .inp files from simple Python parameters.

Units written into the namelist match LEWICE 3.2:
  chord-normalized geometry, CHORD in meters, VINF in m/s, TINF in K,
  PINF in Pa, LWC in g/m^3, DPD (MVD) in micrometers, TSTOP in seconds.

IFLO is the number of icing updates (the flow field is recomputed that many
times). It is not a flow-solver switch. Distribution Example 1 uses IFLO = 6
on a 360 s exposure, i.e. a 60 s step, and the IRT validation inputs do the
same. NPL is left at 24, as in those inputs; it is not the time-step count.
"""
import math
import os

# Default LEWICE parameters. IFLO/NPL/DSMN match Inputs/case1.inp.
DEFAULTS = {
    "TSTOP": 360.0,       # Icing exposure time (seconds)
    "IBOD": 1,            # Number of bodies
    "IFLO": 6,            # Number of icing updates (flow recomputed each update)
    "DSMN": 4.0e-4,       # Minimum panel size, chord-normalized
    "NPL": 24,            # Trajectory / discretization control (LEWICE default)
    "CHORD": 0.9144,      # Chord length (meters)
    "AOA": 0.0,           # Angle of attack (degrees)
    "VINF": 90.0,         # Freestream velocity (m/s)
    "LWC": 0.5,           # Liquid water content (g/m^3)
    "TINF": 263.15,       # Freestream temperature (K) = -10 C
    "PINF": 100000.0,     # Freestream pressure (Pa)
    "RH": 100.0,          # Relative humidity (%)
    "FLWC": 1.0,          # Droplet distribution fraction(s)
    "DPD": 20.0,          # Droplet diameter(s) (micrometers / MVD)
}

# One icing update per minute matches the validation inputs, and the 6-minute
# studio default stays at IFLO = 6. The cap keeps a 45-minute case from asking
# for 45 potential-flow solutions.
_ICING_STEP_S = 60.0
_MAX_ICING_STEPS = 24

def celsius_to_kelvin(c):
    return c + 273.15

def fahrenheit_to_kelvin(f):
    return (f - 32) * 5 / 9 + 273.15

def ktas_to_ms(ktas):
    """True airspeed: 1 knot = 1852 m / 3600 s."""
    return ktas * (1852.0 / 3600.0)

def feet_to_meters(ft):
    return ft * 0.3048

def altitude_to_pressure(alt_ft):
    """International Standard Atmosphere static pressure (Pa) from geometric altitude (ft).

    Troposphere (0 to 11 km) uses the usual lapse-rate formula. From 11 km to
    20 km the temperature is constant at 216.65 K, so the old single formula
    (which kept cooling past the tropopause) is not used above 36,089 ft.
    """
    h = feet_to_meters(float(alt_ft))
    if h < 0.0:
        h = 0.0
    p0 = 101325.0
    t0 = 288.15
    lapse = 0.0065
    g = 9.80665
    R = 287.05287
    h_trop = 11000.0
    exponent = g / (R * lapse)
    if h <= h_trop:
        return p0 * (1.0 - lapse * h / t0) ** exponent
    p_trop = p0 * (1.0 - lapse * h_trop / t0) ** exponent
    t_trop = t0 - lapse * h_trop
    # ISA 11-20 km layer. Above 20 km this is no longer the standard model;
    # the sidebar altitude stops at 45,000 ft (13.7 km), inside this layer.
    return p_trop * math.exp(-g * (h - h_trop) / (R * t_trop))


def icing_steps(exposure_s, step_s=_ICING_STEP_S, max_steps=_MAX_ICING_STEPS):
    """Number of IFLO icing updates for an exposure, about one per minute."""
    steps = int(math.floor(float(exposure_s) / float(step_s) + 0.5))
    if steps < 1:
        steps = 1
    if steps > max_steps:
        steps = max_steps
    return steps

def build_input(params, title="LEWICE Studio Run"):
    """Generate a LEWICE .inp file string from a parameter dict."""
    p = {**DEFAULTS, **params}

    # Handle droplet distribution (can be list or single value)
    flwc = p["FLWC"]
    dpd = p["DPD"]
    if isinstance(flwc, (list, tuple)):
        flwc_str = ", ".join(f"{v}" for v in flwc)
        dpd_str = ", ".join(f"{v}" for v in dpd)
    else:
        flwc_str = str(flwc)
        dpd_str = str(dpd)

    # LEWICE's own examples use a Fortran D exponent (4.0D-4).
    dsmn_mant, dsmn_exp = f"{float(p['DSMN']):.1E}".split("E")
    dsmn_str = f"{float(dsmn_mant):.1f}D{int(dsmn_exp)}"

    safe_title = " ".join(str(title).split())
    safe_title = safe_title.replace("&", " ").strip() or "LEWICE Studio Run"

    inp = f""" {safe_title}
 &LEW20
 TSTOP  = {p['TSTOP']:.1f}
 IBOD   = {p['IBOD']}
 IFLO   = {int(p['IFLO'])}
 DSMN   = {dsmn_str}
 NPL    = {int(p['NPL'])}
 &END
 &DIST
 FLWC   = {flwc_str}
 DPD    = {dpd_str}
 &END
 &ICE1
 CHORD  = {p['CHORD']:.4f}
 AOA    = {p['AOA']:.1f}
 VINF   = {p['VINF']:.1f}
 LWC    = {p['LWC']:.3f}
 TINF   = {p['TINF']:.2f}
 PINF   = {p['PINF']:.2f}
 RH     = {p['RH']:.1f}
 &END
 &LPRNT
 FPRT   = 1
 HPRT   = 1
 BPRT   = 1
 TPRT   = 0
 &END
 &RDATA
 &END
 &BOOT
 &END
"""
    return inp

def write_input(filepath, params, title="LEWICE Studio Run"):
    """Write a LEWICE input file to disk."""
    content = build_input(params, title)
    with open(filepath, "w") as f:
        f.write(content)
    return filepath

def build_case_from_friendly(
    chord_m=0.9144,
    aoa_deg=0.0,
    speed_ktas=None,
    speed_ms=None,
    altitude_ft=None,
    pressure_pa=None,
    temp_c=None,
    temp_k=None,
    lwc=0.5,
    mvd=20.0,
    exposure_min=6.0,
    time_steps=None,
):
    """Build a LEWICE param dict from friendly engineering units."""
    params = {}
    params["CHORD"] = chord_m
    params["AOA"] = aoa_deg
    params["TSTOP"] = exposure_min * 60.0
    # time_steps used to be written into NPL. NPL is not the icing-step count;
    # IFLO is. Honor an explicit time_steps override as IFLO, otherwise use
    # one update per minute (6 on the 6-minute default, same as Example 1).
    if time_steps is None:
        params["IFLO"] = icing_steps(params["TSTOP"])
    else:
        params["IFLO"] = max(1, int(time_steps))
    params["NPL"] = DEFAULTS["NPL"]
    params["LWC"] = lwc
    params["DPD"] = mvd
    params["FLWC"] = 1.0

    # Speed
    if speed_ms is not None:
        params["VINF"] = speed_ms
    elif speed_ktas is not None:
        params["VINF"] = ktas_to_ms(speed_ktas)
    else:
        params["VINF"] = 90.0

    # Temperature
    if temp_k is not None:
        params["TINF"] = temp_k
    elif temp_c is not None:
        params["TINF"] = celsius_to_kelvin(temp_c)
    else:
        params["TINF"] = celsius_to_kelvin(-10.0)

    # Pressure
    if pressure_pa is not None:
        params["PINF"] = pressure_pa
    elif altitude_ft is not None:
        params["PINF"] = altitude_to_pressure(altitude_ft)
    else:
        params["PINF"] = 101325.0

    return params


if __name__ == "__main__":
    # Quick test
    params = build_case_from_friendly(
        chord_m=0.9144,
        aoa_deg=4.5,
        speed_ktas=175,
        altitude_ft=10000,
        temp_c=-10,
        lwc=0.54,
        mvd=20.0,
        exposure_min=6.0,
    )
    print(build_input(params, "Test Case - LEWICE Studio"))
