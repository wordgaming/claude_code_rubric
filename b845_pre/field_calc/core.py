import math

EPSILON_0 = 8.8541878128e-12

def electric_flux(q):
    flux = q / EPSILON_0  #point charge total flux
    print(f"Electric flux: {flux:.3e} N·m²/C")
    return flux

def electric_field(q, r='r'):
    if isinstance(r, str) and r == 'r':
        const = q / (4 * math.pi * EPSILON_0)
        print(f"Electric field: {const:.3e}/(r**2) N/C")
        return const
    else:
        E = q / (4 * math.pi * EPSILON_0 * r * r)  #find electric field at r
        print(f"Electric field at r={r} m: {E:.3e} N/C")
        return E
