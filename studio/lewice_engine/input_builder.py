"""
LEWICE Input Builder
Generates valid LEWICE .inp files from simple Python parameters.
"""
import os

# Default LEWICE parameters
DEFAULTS = {
    "TSTOP": 360.0,       # Icing exposure time (seconds)
    "IBOD": 1,            # Number of bodies
    "IFLO": 6,            # Flow solver (6 = panel method)
    "DSMN": 4.0e-4,       # Minimum panel size
    "NPL": 24,            # Number of time steps
    "CHORD": 0.9144,      # Chord length (meters)
    "AOA": 0.0,           # Angle of attack (degrees)
    "VINF": 90.0,         # Freestream velocity (m/s)
    "LWC": 0.5,           # Liquid water content (g/m3)
    "TINF": 263.15,       # Freestream temperature (K) = -10C
    "PINF": 100000.0,     # Freestream pressure (Pa)
    "RH": 100.0,          # Relative humidity (%)
    "FLWC": 1.0,          # Droplet distribution fraction(s)
    "DPD": 20.0,          # Droplet diameter(s) (microns / MVD)
}

def celsius_to_kelvin(c):
    return c + 273.15

def fahrenheit_to_kelvin(f):
    return (f - 32) * 5 / 9 + 273.15

def ktas_to_ms(ktas):
    return ktas * 0.514444

def feet_to_meters(ft):
    return ft * 0.3048

def altitude_to_pressure(alt_ft):
    """ISA pressure from altitude (feet) — simple model."""
    alt_m = feet_to_meters(alt_ft)
    return 101325 * (1 - 2.25577e-5 * alt_m) ** 5.25588

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

    inp = f""" {title}
 &LEW20
 TSTOP  = {p['TSTOP']:.1f}
 IBOD   = {p['IBOD']}
 IFLO   = {p['IFLO']}
 DSMN   = {p['DSMN']:.1E}
 NPL    = {p['NPL']}
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
    time_steps=24,
):
    """Build a LEWICE param dict from friendly engineering units."""
    params = {}
    params["CHORD"] = chord_m
    params["AOA"] = aoa_deg
    params["NPL"] = time_steps
    params["TSTOP"] = exposure_min * 60.0
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
