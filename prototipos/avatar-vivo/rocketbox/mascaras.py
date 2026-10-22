# Rasteriza en el espacio UV de la textura de la cara un peso por vértice
# (interpolado en cada triángulo) para obtener máscaras de zona.
import numpy as np
def rasterizar(tris, tuv, w, lado):
    M = np.zeros((lado, lado), np.float32)
    for t, uv in zip(tris, tuv):
        p = np.array([[u * lado, (1 - v) * lado] for u, v in uv])
        x0, y0 = np.floor(p.min(0)).astype(int); x1, y1 = np.ceil(p.max(0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, lado - 1), min(y1, lado - 1)
        if x1 < x0 or y1 < y0: continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
        (ax, ay), (bx, by), (cx, cy) = p
        d = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(d) < 1e-9: continue
        l1 = ((by - cy) * (xs - cx) + (cx - bx) * (ys - cy)) / d
        l2 = ((cy - ay) * (xs - cx) + (ax - cx) * (ys - cy)) / d
        l3 = 1 - l1 - l2
        dentro = (l1 >= -1e-3) & (l2 >= -1e-3) & (l3 >= -1e-3)
        val = l1 * w[t[0]] + l2 * w[t[1]] + l3 * w[t[2]]
        sub = M[y0:y1 + 1, x0:x1 + 1]
        sub[dentro] = np.maximum(sub[dentro], val[dentro])
    return M
