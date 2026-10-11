import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent / "graficas"
OUT.mkdir(exist_ok=True)
w = np.logspace(-2, 2, 3000)
s = 1j*w
D = s**2 + np.sqrt(2)*s + 1
responses = {
    "a_paso_bajo": 1/D,
    "b_paso_alto": (s**2 + np.sqrt(2)*s)/D,
    "c_paso_banda": np.sqrt(2)*s/D,
}
wc_b = np.sqrt(np.sqrt(5)-2)
w1 = np.sqrt(1.5)-1/np.sqrt(2)
w2 = np.sqrt(1.5)+1/np.sqrt(2)
for name, H in responses.items():
    fig, axes = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True, layout="constrained")
    magnitude = 20*np.log10(np.abs(H))
    phase = np.angle(H, deg=True)
    axes[0].semilogx(w, magnitude, linewidth=2, label="Respuesta exacta")
    if name.startswith("a"):
        asym = np.where(w <= 1, 0, -40*np.log10(w))
        cuts = [1]
        title = "a) Filtro paso bajo"
    elif name.startswith("b"):
        # Asintota por polos y ceros: cero en 0, cero en sqrt(2), dos polos en |s|=1.
        asym = 20*np.log10(np.sqrt(2)*w) + 20*np.log10(np.maximum(1, w/np.sqrt(2))) - 40*np.log10(np.maximum(1, w))
        cuts = [wc_b]
        title = "b) Filtro paso alto con realce"
    else:
        asym = np.where(w <= 1, 20*np.log10(np.sqrt(2)*w), 20*np.log10(np.sqrt(2)/w))
        cuts = [w1, w2]
        title = "c) Filtro paso banda"
    axes[0].semilogx(w, asym, "--", label="Aproximación asintótica")
    for k, cut in enumerate(cuts):
        axes[0].axvline(cut, color="gray", linestyle=":", alpha=.65, label="Frecuencia de corte" if k==0 else None)
    axes[0].set_ylabel("Módulo (dB)")
    axes[0].set_title(title)
    axes[0].legend()
    axes[0].grid(True, which="both", alpha=.25)
    axes[1].semilogx(w, phase, linewidth=2, label="Fase exacta")
    axes[1].set_xlabel("Frecuencia angular ω (rad/s)")
    axes[1].set_ylabel("Fase (°)")
    axes[1].grid(True, which="both", alpha=.25)
    axes[1].legend()
    fig.savefig(OUT / f"{name}.png", dpi=180)
    plt.close(fig)

print(f"Circuito a: ωc = 1 rad/s; BW = 1 rad/s")
print(f"Circuito b: ωc = {wc_b:.6f} rad/s; BW ideal = infinito")
print(f"Circuito c: ω1 = {w1:.6f}, ω2 = {w2:.6f}; BW = {w2-w1:.6f} rad/s")
