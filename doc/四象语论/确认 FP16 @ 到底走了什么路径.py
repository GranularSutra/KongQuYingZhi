import numpy as np, time
rng = np.random.default_rng(0)
W = rng.standard_normal((50000, 768)).astype(np.float16)
q = rng.standard_normal(768).astype(np.float16)
t0 = time.perf_counter(); s = W @ q; print("fp16 @:", time.perf_counter()-t0, "s, dtype=", s.dtype)
W32 = W.astype(np.float32); q32 = q.astype(np.float32)
t0 = time.perf_counter(); s = W32 @ q32; print("fp32 @:", time.perf_counter()-t0, "s, dtype=", s.dtype)