"""
pytest configuration for KevinNet DNS tests.

The main `kevinnet.py` file imports tkinter at module level. When tkinter
is not available (CI containers without X server, or headless Linux), the
module sys.exit()s. To run unit tests on pure-function code we monkey-patch
sys.modules with stubs BEFORE the test imports kevinnet.

This is a workaround until kevinnet.py is split into modules (planned for
a later release). Once the GUI lives in its own module, tests will import
the pure-logic modules directly without this trick.
"""
import sys
import types
from pathlib import Path

# Make the project root importable so `import kevinnet` works regardless
# of where pytest is invoked from.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _stub_tkinter():
    """Install minimal tkinter stubs so kevinnet imports cleanly.

    The bidi monkey-patch in kevinnet runs at import time and patches
    methods like `configure`, `config`, `insert` on widget classes — our
    stubs must therefore expose those attributes as plain callables, not
    just allow `__getattr__` access. A real class with no-op methods
    works; instance-level `__getattr__` does not.
    """
    if "tkinter" in sys.modules:
        return

    tk = types.ModuleType("tkinter")

    def _make_widget_class(name):
        """Build a class that satisfies tk widget assumptions:
           - instantiable with arbitrary args
           - has callable configure/config/cget/insert/delete/winfo_*/bind etc.
           - both class- and instance-level attribute access returns a no-op
        """
        def _noop(self, *a, **kw):
            return None

        attrs = {"__init__": lambda self, *a, **kw: None}
        for m in ("configure", "config", "cget", "insert", "delete",
                  "pack", "pack_propagate", "grid", "grid_propagate",
                  "place", "destroy", "update", "update_idletasks",
                  "bind", "unbind", "winfo_children", "winfo_x",
                  "winfo_y", "winfo_width", "winfo_height",
                  "winfo_screenheight", "winfo_screenwidth",
                  "winfo_reqheight", "winfo_reqwidth", "title",
                  "geometry", "minsize", "maxsize", "resizable",
                  "iconphoto", "wm_iconphoto", "after", "after_idle",
                  "mainloop", "tk_popup", "grab_set", "grab_release",
                  "get_children", "selection", "selection_set",
                  "identify_row", "item", "heading", "column",
                  "tag_configure", "yview", "yview_scroll", "bbox",
                  "create_window", "itemconfig", "set", "get",
                  "see", "focus_set", "tag_remove", "tag_add",
                  "tag_bind", "index", "compare", "lift", "lower",
                  "withdraw", "deiconify", "iconify"):
            attrs[m] = _noop
        # Tk-style return-value methods that callers may use
        attrs["winfo_exists"] = lambda self: True
        cls = type(name, (object,), attrs)
        return cls

    for name in ("Tk", "Toplevel", "Frame", "Label", "Button", "Canvas",
                 "Checkbutton", "Radiobutton", "Menu", "Text", "Entry",
                 "PanedWindow", "Listbox", "Scale", "Spinbox"):
        setattr(tk, name, _make_widget_class(name))

    # Variable classes — get/set must round-trip
    class _Var:
        def __init__(self, master=None, value=None, name=None):
            self._v = value
        def get(self): return self._v
        def set(self, v): self._v = v
        def trace_add(self, *a, **kw): pass
        def trace(self, *a, **kw): pass
    tk.StringVar  = type("StringVar",  (_Var,), {})
    tk.BooleanVar = type("BooleanVar", (_Var,), {})
    tk.IntVar     = type("IntVar",     (_Var,), {})
    tk.DoubleVar  = type("DoubleVar",  (_Var,), {})

    tk.TclError = type("TclError", (Exception,), {})
    # Constants the code may reference
    for k in ("NORMAL", "DISABLED", "END", "INSERT", "CENTER", "W", "E",
              "N", "S", "NS", "EW", "NSEW", "LEFT", "RIGHT", "TOP", "BOTTOM",
              "BOTH", "X", "Y", "NONE", "HORIZONTAL", "VERTICAL"):
        setattr(tk, k, k.lower())
    sys.modules["tkinter"] = tk

    ttk = types.ModuleType("tkinter.ttk")
    for name in ("Treeview", "Scrollbar", "Style", "Progressbar",
                 "Notebook", "Label", "Frame", "Entry", "Combobox",
                 "Separator", "Button", "Checkbutton"):
        setattr(ttk, name, _make_widget_class(name))
    sys.modules["tkinter.ttk"] = ttk

    mb = types.ModuleType("tkinter.messagebox")
    for fn in ("showinfo", "showwarning", "showerror",
               "askokcancel", "askyesno", "askretrycancel", "askquestion"):
        setattr(mb, fn, lambda *a, **kw: None)
    sys.modules["tkinter.messagebox"] = mb

    st = types.ModuleType("tkinter.scrolledtext")
    st.ScrolledText = _make_widget_class("ScrolledText")
    sys.modules["tkinter.scrolledtext"] = st

    sd = types.ModuleType("tkinter.simpledialog")
    sd.askstring = lambda *a, **kw: None
    sys.modules["tkinter.simpledialog"] = sd

    font = types.ModuleType("tkinter.font")
    font.families = lambda: ()
    font.Font = _make_widget_class("Font")
    sys.modules["tkinter.font"] = font

    fd = types.ModuleType("tkinter.filedialog")
    fd.asksaveasfilename = lambda *a, **kw: ""
    fd.askopenfilename   = lambda *a, **kw: ""
    fd.askdirectory      = lambda *a, **kw: ""
    sys.modules["tkinter.filedialog"] = fd


_stub_tkinter()
