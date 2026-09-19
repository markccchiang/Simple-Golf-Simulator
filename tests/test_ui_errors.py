import pytest

import Plot
import Plot2
import UIFunc


class FakeEntry:
    """Stands in for a ttk.Entry / StringVar: just a value, and optionally a label."""
    def __init__(self, value, label=None):
        self.value = value
        if label is not None:
            self.label = label

    def get(self):
        return self.value

    def delete(self, first, last):
        self.value = ''

    def insert(self, index, value):
        self.value = value


@pytest.fixture
def dialogs(monkeypatch):
    """Capture (title, message) of every error dialog instead of opening one."""
    shown = []
    monkeypatch.setattr(UIFunc.messagebox, 'showerror', lambda title, msg: shown.append((title, msg)))
    return shown


def test_get_float_names_the_field_in_its_error():
    entries = {'phi': FakeEntry('sixty', label='9. Swing plane angle (deg)')}
    with pytest.raises(UIFunc.UserFacingError, match=r'"9\. Swing plane angle \(deg\)" must be a number, but it is "sixty"'):
        UIFunc.get_float(entries, 'phi')


def test_require_result_explains_which_step_to_run_first():
    entries = {'Q_beta': FakeEntry('N/A')}
    with pytest.raises(UIFunc.UserFacingError, match='Optimize'):
        UIFunc.require_result(entries, 'Q_beta', 'Click "Optimize wrist-cock torque" first.')


def test_math_errors_are_reported_as_simulation_errors_not_bad_input(dialogs):
    @UIFunc.validate_inputs
    def callback(entries):
        raise ValueError('math domain error')

    callback({})
    title, msg = dialogs[0]
    assert title == 'Simulation Error'
    assert 'math domain error' in msg
    assert 'must be a number' not in msg


def test_simulation_runtime_errors_are_shown_verbatim(dialogs):
    @UIFunc.validate_inputs
    def callback(entries):
        raise RuntimeError('Launch speed must be positive.')

    callback({})
    assert dialogs == [('Simulation Error', 'Launch speed must be positive.')]


def test_launch_calculation_before_swing_says_to_simulate_the_swing(dialogs):
    entries = {'M_C_head': FakeEntry('0.2'), 'ball_mass': FakeEntry('0.0458'),
               'COR': FakeEntry('0.775'), 'VC': FakeEntry('N/A')}
    Plot.get_ball_velocity(entries)
    assert dialogs == [('Input Error', Plot.SWING_HINT)]


def test_ball_flight_before_launch_calculation_says_which_button_to_click(dialogs):
    entries = {key: FakeEntry('0') for key in
               ('ball_mass', 'ball_diameter', 'COR', 'C_D', 'C_L', 'rho_air',
                'v_wind', 'wind_theta', 'wind_phi')}
    entries['ball_U'] = FakeEntry('N/A')
    Plot2.Plot(entries)
    assert dialogs == [('Input Error', Plot2.LAUNCH_HINT)]


def test_shoulder_radius_not_smaller_than_arm_length_is_rejected_before_simulating(dialogs):
    entries = {'Gender': FakeEntry('Male'), 'Weight': FakeEntry('70'),
               'R_S': FakeEntry('0.7'), 'R_A': FakeEntry('0.6')}
    Plot.Plot(entries)
    title, msg = dialogs[0]
    assert title == 'Input Error'
    assert 'shoulder radius (item 3)' in msg


# --- Wrist-cock torque optimization ------------------------------------------

SWING_DEFAULTS = dict(Gender='Male', Weight='70', R_S='0.17', R_A='0.6', M_C_head='0.2', M_C_shaft='0.1',
                      L_C_head='0.1', L_C_shaft='1.0', phi='60', theta='135', theta_final='0', beta='120',
                      beta_final='0', a_x='0', a_y='0', Type='Type I', Q_alpha='100', tau_Q_alpha='0.01',
                      set_theta='135', tau_Q_beta='0.01', Q_beta_min='-50', Q_beta_max='0',
                      Method='Solution 4', Q_beta='N/A')


def swing_entries(**overrides):
    return {key: FakeEntry(value) for key, value in {**SWING_DEFAULTS, **overrides}.items()}


def test_best_torque_is_the_closest_of_all_tries_not_just_better_than_the_previous_one():
    # Tried torques 0, -1, -2, -3 N-m (stored negated) with impact wrist-cock angles 10, 0.1, 5, -3 degree.
    # Comparing each try only with the previous one would pick -3 N-m; the closest to 0 degree is -1 N-m.
    assert Plot._best_Q_beta([0.0, 1.0, 2.0, 3.0], [10.0, 0.1, 5.0, -3.0], 0.0, -50.0, 0.0) == -1.0


def test_best_torque_ignores_tries_outside_the_allowed_range():
    # -2 N-m hits the target exactly but lies outside the range [-1, 0]; -1 N-m is the best allowed try.
    assert Plot._best_Q_beta([0.0, 1.0, 2.0], [5.0, -1.0, 0.0], 0.0, -1.0, 0.0) == -1.0


def test_optimizer_finds_the_default_wrist_cock_torque(dialogs):
    entries = swing_entries()
    Plot.Optimize_Q_beta(entries)
    assert dialogs == []
    assert entries['Q_beta'].get() == '-20.62'


def test_optimizer_reports_a_target_out_of_range_instead_of_a_wrong_torque(dialogs):
    # Previously the fast optimizer silently reported 0.00 N-m here.
    entries = swing_entries(Q_beta_min='-10')
    Plot.Optimize_Q_beta(entries)
    title, msg = dialogs[0]
    assert title == 'Input Error'
    assert 'Lower the minimum wrist-cock torque (item 22)' in msg
    assert entries['Q_beta'].get() == ''


def test_optimizer_rejects_a_reversed_torque_range(dialogs):
    entries = swing_entries(Q_beta_min='0', Q_beta_max='-50')
    Plot.Optimize_Q_beta_2(entries)
    assert dialogs == [('Input Error', 'The minimum wrist-cock torque (item 22) must not be greater than '
                                       'the maximum (item 23).')]


# --- Busy cursor ---------------------------------------------------------------

class FakeWindow:
    def __init__(self):
        self.cursor = ''
        self.cursor_during_dialog = None

    def config(self, cursor):
        self.cursor = cursor

    def update_idletasks(self):
        pass


class FakeWidget(FakeEntry):
    def __init__(self, value, window):
        super().__init__(value)
        self.window = window

    def winfo_toplevel(self):
        return self.window


def test_busy_cursor_is_shown_while_a_callback_runs():
    window = FakeWindow()
    seen = []

    @UIFunc.validate_inputs
    def callback(entries):
        seen.append(window.cursor)

    callback({'x': FakeWidget('1', window)})
    assert seen == ['watch']
    assert window.cursor == ''


def test_busy_cursor_is_cleared_before_an_error_dialog(monkeypatch):
    window = FakeWindow()
    monkeypatch.setattr(UIFunc.messagebox, 'showerror',
                        lambda title, msg: setattr(window, 'cursor_during_dialog', window.cursor))

    @UIFunc.validate_inputs
    def callback(entries):
        raise UIFunc.UserFacingError('bad input')

    callback({'x': FakeWidget('1', window)})
    assert window.cursor_during_dialog == ''
