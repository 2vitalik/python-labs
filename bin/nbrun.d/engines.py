"""The two ways a notebook runs inside the box (T354): each puts the executed notebook into state["nb"] and returns a note
on what went wrong beyond the cells' own errors ("" — nothing)."""
import json
import os
import subprocess

WORK = "/tmp/work"
KEPT = 10 * 2**20  # bytes of outputs kept: a flood is cut here, not in the frame's memory
DOOMED = 1000  # oom_score_adj of the notebook's processes: out of memory, the kernel goes first, not the frame


def doomed(pid: int) -> None:
    """The notebook's processes (and all they spawn) lose to the frame: first to die of memory, last to get the CPU."""
    with open(f"/proc/{pid}/oom_score_adj", "w") as f:
        f.write(str(DOOMED))
    os.setpriority(os.PRIO_PROCESS, pid, 19)


def ipynb(src: bytes, state: dict) -> str:
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import DeadKernelError

    class Client(NotebookClient):
        room = KEPT

        def output(self, outs, msg, display_id, cell_index):
            self.room -= len(json.dumps(msg["content"]))
            if self.room >= 0:
                return super().output(outs, msg, display_id, cell_index)
            if not getattr(self, "cut", False):
                self.cut = True
                outs.append(nbformat.v4.new_output("stream", name="stderr", text=f"… вивід понад {KEPT >> 20} МБ обрізано\n"))

    def timed_out(cell, cell_index, execute_reply):  # nbclient's own timeout reply leaves no error in the outputs
        c = execute_reply["content"]
        if c.get("status") == "error" and not any(o.output_type == "error" for o in cell.outputs):
            cell.outputs.append(nbformat.v4.new_output("error", ename=c.get("ename", ""), evalue=c.get("evalue", ""),
                                                       traceback=[]))

    state["nb"] = nb = nbformat.reads(src.decode(), as_version=4)  # filled in place: the frame sees it even if we hang
    os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"  # figures become outputs, as in Colab
    client = Client(nb, timeout=120, kernel_name="python3", allow_errors=True, interrupt_on_timeout=True,
                    error_on_timeout={"ename": "Timeout", "evalue": "клітинка довша за 120 с — перервано", "traceback": []},
                    on_cell_executed=timed_out, on_notebook_start=lambda **_: doomed(client.km.provisioner.pid),
                    resources={"metadata": {"path": WORK}})
    try:
        client.execute()
    except DeadKernelError:
        return "ядро Python зупинилось посеред роботи" + oom()
    return ""


def marimo(src: bytes, state: dict) -> str:
    path, out = f"{WORK}/notebook.py", "/tmp/executed.ipynb"
    with open(path, "wb") as f:
        f.write(src)
    r = subprocess.run(["sh", "-c", f'echo {DOOMED} > /proc/self/oom_score_adj && exec nice -n 19 "$@"', "sh",
                        "marimo", "-y", "export", "ipynb", path, "--include-outputs", "--sort", "top-down", "-f", "-o", out],
                       cwd=WORK, stdin=subprocess.DEVNULL, check=False)
    if not os.path.exists(out) or os.path.getsize(out) > 4 * KEPT:
        return f"marimo не дав виконаного ноутбука (код {r.returncode})" + oom()
    with open(out, encoding="utf-8") as f:
        state["nb"] = nb = json.load(f)
    failed = any(o.get("output_type") == "error" for c in nb.get("cells", []) for o in c.get("outputs", []))
    if r.returncode == 0 or r.returncode == 1 and failed:  # 1 — "some cells failed": their errors are in the outputs
        return ""
    return f"marimo завершився з кодом {r.returncode}" + oom()


def oom() -> str:
    try:
        with open("/sys/fs/cgroup/memory.events") as f:
            killed = int(dict(l.split() for l in f).get("oom_kill", 0))
    except OSError:
        return ""
    return " · забракло памʼяті (1 ГБ)" if killed else ""


def swarm() -> bool:
    """Half the process limit is taken: a fork bomb gets there in a second, a lab notebook keeps under ~40."""
    try:
        with open("/sys/fs/cgroup/pids.current") as now, open("/sys/fs/cgroup/pids.max") as top:
            return int(now.read()) >= int(top.read()) // 2
    except (OSError, ValueError):
        return False
