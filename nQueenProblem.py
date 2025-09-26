import streamlit as st
import time

# ---------- Core logic ----------
def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

def build_trace(n):
    """สร้างลิสต์ moves แบบละเอียดทุกสเต็ป: try / fail / backtrack / solution"""
    moves = []
    board = [-1]*n

    def dfs(row=0):
        if row == n:
            moves.append(("solution", board[:], row, None))
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                moves.append(("try", board[:], row, col))
                dfs(row+1)
                board[row] = -1
                moves.append(("backtrack", board[:], row, col))
            else:
                moves.append(("fail", board[:], row, col))
    dfs(0)
    return moves

def draw_board(board, n):
    lines = []
    for r in range(n):
        row = []
        for c in range(n):
            row.append("Q" if board[r] == c else ".")
        lines.append(" ".join(row))
    return "\n".join(lines)

# ---------- UI ----------
st.title("♛ N-Queens — Live Animation + Full Trace")

# Controls (persist)
if "n" not in st.session_state:
    st.session_state.n = 4
if "moves" not in st.session_state:
    st.session_state.moves = []
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "trace" not in st.session_state:
    st.session_state.trace = []
if "speed" not in st.session_state:
    st.session_state.speed = 0.5

# Pick board size & speed
n = st.slider("ขนาดกระดาน (n)", 4, 10, st.session_state.n)
speed = st.slider("⏱️ ความเร็ว (วินาที/สเต็ป)", 0.05, 2.0, st.session_state.speed, 0.05)

# When n/speed changed, store
if n != st.session_state.n:
    st.session_state.n = n
    st.session_state.moves = build_trace(n)
    st.session_state.idx = 0
    st.session_state.trace = []
    st.session_state.running = False
st.session_state.speed = speed

# Initial build if missing
if not st.session_state.moves:
    st.session_state.moves = build_trace(st.session_state.n)
    st.session_state.idx = 0
    st.session_state.trace = []
    st.session_state.running = False

# Buttons (actions)
cols = st.columns(4)
with cols[0]:
    if st.button("▶️ Start", use_container_width=True):
        st.session_state.running = True
with cols[1]:
    if st.button("⏸️ Stop", use_container_width=True):
        st.session_state.running = False
with cols[2]:
    if st.button("➡️ Next", use_container_width=True):
        st.session_state.running = False
        if st.session_state.idx < len(st.session_state.moves):
            st.session_state.idx += 1
with cols[3]:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.moves = build_trace(st.session_state.n)
        st.session_state.idx = 0
        st.session_state.trace = []
        st.session_state.running = False

# Current frame
idx = st.session_state.idx
moves = st.session_state.moves
n = st.session_state.n

# Derive board for current frame
board_view = [-1]*n
msg = "เริ่มต้น"
if idx > 0:
    kind, bd, row, col = moves[idx-1]
    board_view = bd
    if kind == "try":
        msg = f"✅ วาง (row={row}, col={col})"
    elif kind == "fail":
        msg = f"❌ ไม่ปลอดภัย (row={row}, col={col})"
    elif kind == "backtrack":
        msg = f"🔙 Backtrack (row={row}, col={col})"
    elif kind == "solution":
        msg = "🎉 พบคำตอบ (Solution)"

# Render board + status
st.markdown(f"**Step {idx}/{len(moves)}** — {msg}")
st.text(draw_board(board_view, n))

# Live trace (current steps)
st.subheader("📜 Trace Log (สด)")
log_container = st.container()
with log_container:
    # Append new logs up to idx
    # Ensure trace length matches idx
    while len(st.session_state.trace) < idx:
        k, bd, r, c = moves[len(st.session_state.trace)]
        if k == "try":
            st.session_state.trace.append(f"{len(st.session_state.trace)+1:>4}: ✅ TRY     (row={r}, col={c})")
        elif k == "fail":
            st.session_state.trace.append(f"{len(st.session_state.trace)+1:>4}: ❌ FAIL    (row={r}, col={c})")
        elif k == "backtrack":
            st.session_state.trace.append(f"{len(st.session_state.trace)+1:>4}: 🔙 BACK    (row={r}, col={c})")
        elif k == "solution":
            st.session_state.trace.append(f"{len(st.session_state.trace)+1:>4}: 🎉 SOLUTION")
    for line in st.session_state.trace[-400:]:  # limit display if huge
        st.write(line)

# Auto "tick" one step per run if running
if st.session_state.running and st.session_state.idx < len(st.session_state.moves):
    # sleep ตาม speed แล้วขยับหนึ่งสเต็ป
    time.sleep(st.session_state.speed)
    st.session_state.idx += 1
    # ให้สคริปต์รันใหม่เพื่ออ่านสถานะปุ่ม (Stop) และวาดเฟรมถัดไป
    st.rerun()

# ถ้าจบหมดแล้ว หยุดอัตโนมัติ
if st.session_state.idx >= len(st.session_state.moves):
    st.session_state.running = False