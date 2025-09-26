import streamlit as st
import time

# Recursive Hanoi: บันทึก moves ทั้งหมด
def hanoi(n, source, aux, dest, moves):
    if n == 1:
        moves.append((1, source, dest))
        return
    hanoi(n-1, source, dest, aux, moves)
    moves.append((n, source, dest))
    hanoi(n-1, aux, source, dest, moves)

# ฟังก์ชันวาดเสา (ASCII)
def draw_pegs(pegs, n):
    max_disk = n
    output = ""
    for level in range(n-1, -1, -1):
        for peg in pegs:
            if level < len(peg):
                disk = peg[level]
                pad = " " * (max_disk - disk)
                output += pad + "■" * (disk*2-1) + pad + "  "
            else:
                output += " " * max_disk + "|" + " " * max_disk + "  "
        output += "\n"
    return output

st.title("🏗️ Tower of Hanoi (Step / Auto with Trace)")

# เลือกจำนวนดิสก์
n = st.slider("เลือกจำนวนดิสก์", 1, 6, 3)

# init state
if "moves" not in st.session_state or st.session_state.get("n") != n:
    st.session_state.moves = []
    st.session_state.step = 0
    st.session_state.trace = []   # เก็บ log trace
    st.session_state.n = n
    hanoi(n, "A", "B", "C", st.session_state.moves)
    st.session_state.pegs = {
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": []
    }

# Reset
if st.button("🔄 Reset"):
    st.session_state.moves = []
    st.session_state.step = 0
    st.session_state.trace = []
    hanoi(n, "A", "B", "C", st.session_state.moves)
    st.session_state.pegs = {
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": []
    }

# Step
if st.button("➡️ Next Step"):
    if st.session_state.step < len(st.session_state.moves):
        disk, src, dst = st.session_state.moves[st.session_state.step]
        st.session_state.pegs[dst].append(st.session_state.pegs[src].pop())
        st.session_state.step += 1
        st.session_state.trace.append(f"Step {st.session_state.step}: Move disk {disk} {src} → {dst}")

# Auto
if st.button("▶️ Auto Play"):
    placeholder = st.empty()
    for step in range(st.session_state.step, len(st.session_state.moves)):
        disk, src, dst = st.session_state.moves[step]
        st.session_state.pegs[dst].append(st.session_state.pegs[src].pop())
        st.session_state.step += 1
        st.session_state.trace.append(f"Step {st.session_state.step}: Move disk {disk} {src} → {dst}")

        board = draw_pegs(
            [st.session_state.pegs["A"], st.session_state.pegs["B"], st.session_state.pegs["C"]],
            n
        )
        placeholder.text(f"Step {st.session_state.step}/{len(st.session_state.moves)}\n\n{board}")
        time.sleep(0.7)

# แสดงบอร์ดปัจจุบัน
board = draw_pegs(
    [st.session_state.pegs["A"], st.session_state.pegs["B"], st.session_state.pegs["C"]],
    n
)
st.text(f"Step {st.session_state.step}/{len(st.session_state.moves)}")
st.text(board)

# แสดง Trace Log
st.subheader("📜 Trace Log")
for log in st.session_state.trace:
    st.write(log)