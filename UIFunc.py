from tkinter import messagebox

class UserFacingError(Exception):
    """An error whose message is written for the user and shown as-is."""

def validate_inputs(func_to_wrap):
    """Wrap a UI callback so any failure is shown in an error dialog instead of crashing."""
    def wrapper(entries):
        try:
            return func_to_wrap(entries)
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
