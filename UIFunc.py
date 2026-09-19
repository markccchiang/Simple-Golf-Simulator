from tkinter import messagebox

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
    """
    def wrapper(entries):
        window = _window(entries)
        if window is not None:
            window.config(cursor='watch')
            window.update_idletasks()
        try:
            try:
                return func_to_wrap(entries)
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
    """Read a readonly result field that an earlier step fills in; explain which step if it is empty."""
    value = entries[key].get()
    if value == 'N/A':
        raise UserFacingError(hint)
    return float(value)
