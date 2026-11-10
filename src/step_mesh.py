"""Lee un STEP facetado (FACETED_BREP de triángulos + MAPPED_ITEM) y devuelve mallas por parte, en mm."""
import re, sys, numpy as np, trimesh
def load(path):
    ent = {}
    txt = open(path, encoding="latin-1").read()
    for m in re.finditer(r"#(\d+)=([A-Z_0-9]+)\((.*?)\);\s*\n", txt, re.S):
        ent[int(m.group(1))] = (m.group(2), m.group(3))
    refs = lambda s: [int(x) for x in re.findall(r"#(\d+)", s)]
    nums = lambda s: [float(x) for x in re.findall(r"[-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?", s.split("(",1)[1])]
    pt = lambda i: nums(ent[i][1])
    def placement(i):
        o, z, x = refs(ent[i][1])
        o = np.array(pt(o)); z = np.array(pt(z)); x = np.array(pt(x))
        z /= np.linalg.norm(z); x -= z * x.dot(z); x /= np.linalg.norm(x); y = np.cross(z, x)
        T = np.eye(4); T[:3, :3] = np.column_stack([x, y, z]); T[:3, 3] = o; return T
    def brep_mesh(brep):
        shell = refs(ent[brep][1])[0]
        V, F, idx = [], [], {}
        for fs in refs(ent[shell][1]):
            bound = refs(ent[fs][1])[0]             # FACE_OUTER_BOUND
            loop = refs(ent[bound][1])[0]           # POLY_LOOP
            ids = refs(ent[loop][1])
            vi = []
            for p in ids:
                if p not in idx: idx[p] = len(V); V.append(pt(p))
                vi.append(idx[p])
            for k in range(1, len(vi) - 1): F.append([vi[0], vi[k], vi[k + 1]])
        return np.array(V), np.array(F)
    parts = []
    for i, (t, a) in ent.items():
        if t == "MAPPED_ITEM":
            rmap, place = refs(a)
            _, rep = refs(ent[rmap][1])
            brep = [r for r in refs(ent[rep][1]) if r in ent and ent[r][0] == "FACETED_BREP"][0]
            V, F = brep_mesh(brep)
            m = trimesh.Trimesh(V * 1000.0, F, process=True)
            m.apply_transform(np.diag([1, 1, 1, 1.0]) @ _scale_T(placement(place)))
            parts.append((brep, m))
    return parts
def _scale_T(T):
    T = T.copy(); T[:3, 3] *= 1000.0; return T
if __name__ == "__main__":
    for brep, m in load(sys.argv[1]):
        print(brep, len(m.faces), m.is_watertight, np.round(m.extents, 1), round(m.volume / 1000, 2), "cm3")
