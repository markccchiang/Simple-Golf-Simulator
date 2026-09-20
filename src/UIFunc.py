from contextlib import contextmanager
from tkinter import END, messagebox

import matplotlib.pyplot as plt

class UserFacingError(Exception):
    """An error whose message is written for the user and shown as-is."""

def _window(entries):
    """The window holding the entry widgets, or None (e.g. with test doubles)."""
    for widget in entries.values():
        if hasattr(widget, 'winfo_toplevel'):
            return widget.winfo_toplevel()
    return None

def validate_inputs(func_to_wrap):
    """Wrap a UI callback so any failure is shown in an error dialog instead of crashing.

    Shows a busy cursor while the callback runs, since simulations block the window.
    Returns True if the callback finished, False if an error was shown.
    """
    def wrapper(entries):
        window = _window(entries)
        if window is not None:
            window.config(cursor='watch')
            window.update_idletasks()
        try:
            try:
                func_to_wrap(entries)
                return True
            finally:
                if window is not None:
                    window.config(cursor='') # restore before any error dialog appears
        except UserFacingError as e:
            messagebox.showerror("Input Error", str(e))
        except RuntimeError as e:
            messagebox.showerror("Simulation Error", str(e))
        except (ValueError, ArithmeticError) as e:
            messagebox.showerror("Simulation Error",
                "The simulation could not be computed with these inputs (%s).\n\n"
                "Check that the golfer and club dimensions are physically consistent, "
                "e.g. the shoulder radius must be smaller than the arm length." % e)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        return False
    return wrapper

def get_float(entries, key):
    """Read a numeric input field, naming the field if the value is not a number."""
    value = entries[key].get()
    try:
        return float(value)
    except ValueError:
        label = getattr(entries[key], 'label', key)
        raise UserFacingError('"%s" must be a number, but it is "%s".' % (label, value)) from None

def require_result(entries, key, hint):
    """Read a field that an earlier step fills in (or the user types); explain which step if it is empty."""
    if entries[key].get().strip() in ('', 'N/A'):
        raise UserFacingError(hint)
    return get_float(entries, key)

def set_entry(entry, value):
    """Write a value into an Entry (or ResultField), keeping it read-only if it was."""
    try:
        readonly = entry.instate(['readonly'])
        entry.state(['!readonly'])
    except AttributeError:
        readonly = False
    entry.delete(0, END)
    entry.insert(0, value)
    if readonly:
        entry.state(['readonly'])

class ResultField:
    """A result shown as text rather than in an Entry; it offers the Entry methods that
    _set_entry and require_result use, and stores the value in a StringVar."""
    def __init__(self, var):
        self.var = var

    def get(self):
        return self.var.get()

    def delete(self, first, last):
        self.var.set('')

    def insert(self, index, value):
        self.var.set(value)

#
# Each step replaces its own plot windows (by figure number) and shows the new ones; the panel
# runs its steps in a batch, which shows every new plot once at the end.
#
_batch = False
_embedded = False

def use_embedded_plots():
    """The panel shows the figures itself (in tabs), so no plot windows are opened."""
    global _embedded
    _embedded = True

def begin_plots(*numbers):
    for n in numbers:
        plt.close(n)

def show_plots():
    if not _batch and not _embedded:
        plt.show(block=False) # plot windows stay open while the panel keeps working

@contextmanager
def batch_plots():
    global _batch
    _batch = True
    try:
        yield
    finally:
        _batch = False
    if plt.get_fignums() and not _embedded:
        plt.show(block=False)
