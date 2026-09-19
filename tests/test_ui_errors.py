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
