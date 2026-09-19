import numpy as np
import pytest

import AppFunc
import AppFunc2
import BasicFunc


def swing(Q_alpha=100.0, Q_beta=-20.64, phi=60.0, method='Solution 3', swing_type='Type I'):
    """Run the default GUI swing with the given torques, swing plane, solver and swing type."""
    return AppFunc.Tracking(70.0, 0.17, 0.6,
                            0.2, 0.1, 0.1, 1.0,
                            0.0, 0.0, 0.0,
                            Q_alpha, Q_beta, phi, 135.0,
                            0.0, 0.0, 0.0,
                            120.0, 0.0, 0.0,
                            0.0, swing_type, 'Male', method,
                            0.01, 0.01, 135.0)


def convergence_order(values):
    """Observed order p from results at step sizes h, h/2, h/4."""
    a, b, c = values
    return np.log2(abs(a - b) / abs(b - c))


def ball_flight(v_ball=60.0, altitude=0.0):
    """Run the default GUI ball trajectory with the given launch speed and target altitude."""
    return AppFunc2.TRACK(0.0458, 0.0428, 1.2, 0.285, 0.1,
                          v_ball, 15.0, 0.0,
                          0.0, -90.0,
                          0.0, 0.0, 0.0,
                          altitude)


# --- Swing (AppFunc.Tracking) ---------------------------------------------

def test_time_axis_starts_at_zero_and_increments_by_h():
    t = swing()[10]
    assert t[0] == 0.0
    np.testing.assert_allclose(np.diff(t)[:-1], BasicFunc.h)
    assert 0.0 < t[-1] - t[-2] <= BasicFunc.h  # last step is interpolated to the impact


@pytest.mark.parametrize('method', ['Solution 1', 'Solution 2', 'Solution 3', 'Solution 4'])
def test_last_point_is_exactly_at_the_impact_arm_angle(method):
    theta = swing(method=method)[13]
    assert theta[-1] == pytest.approx(0.0, abs=1e-12)  # impact arm angle (item 11) is 0


@pytest.mark.parametrize('swing_type', ['Type I', 'Type II'])
def test_solution_4_is_fourth_order_accurate(monkeypatch, swing_type):
    # Compare the state at a fixed time (not at impact) as the step size is halved.
    alphas = []
    for h in (1e-3, 5e-4, 2.5e-4):
        monkeypatch.setattr(BasicFunc, 'h_RK4', h)
        alpha = swing(method='Solution 4', swing_type=swing_type)[11]
        alphas.append(alpha[round(0.1 / h)])
    assert convergence_order(alphas) == pytest.approx(4.0, abs=0.3)


@pytest.mark.parametrize('swing_type', ['Type I', 'Type II'])
def test_all_solutions_agree_at_impact(swing_type):
    results = [swing(method=m, swing_type=swing_type)
               for m in ('Solution 1', 'Solution 2', 'Solution 3', 'Solution 4')]
    VC = [r[20][-1] for r in results]
    assert max(VC) - min(VC) < 0.1  # m/s


def test_swing_longer_than_one_second_does_not_raise():
    # Previously raised IndexError: rod arrays were sized for at most 1 s of swing.
    t = swing(Q_alpha=1.0, Q_beta=-1.0, phi=10.0)[10]
    assert t[-1] > 1.0


def test_rod_arrays_interleave_start_and_end_points():
    r = swing()
    O_x, arm_x, club_x = r[0], r[2], r[4]
    arm_rod_x, club_rod_x = r[6], r[8]
    assert len(arm_rod_x) == 2 * len(O_x)
    np.testing.assert_array_equal(arm_rod_x[0::2], O_x)
    np.testing.assert_array_equal(arm_rod_x[1::2], arm_x)
    np.testing.assert_array_equal(club_rod_x[0::2], arm_x)
    np.testing.assert_array_equal(club_rod_x[1::2], club_x)


def test_swing_that_never_reaches_impact_raises():
    with pytest.raises(RuntimeError, match="did not reach the impact"):
        swing(Q_alpha=-50.0)


def test_clubhead_speed_is_zero_not_a_string_on_negative_roundoff():
    # With R = 0 and alpha_dot == beta_dot, |V_C|^2 is exactly 0 but rounds to -9.1e-13.
    VC = BasicFunc.func_VC(-36.563575588759875, 1.3897349477489307,
                           -36.563575588759875, 0.0, 1.2637746189766141)
    assert VC == 0.0


# --- Ball flight (AppFunc2.TRACK) ------------------------------------------

def test_ball_lands_at_target_altitude():
    x, y, z = ball_flight()
    assert z[-2] >= 0.0 > z[-1]


def test_very_low_target_altitude_raises_instead_of_index_error():
    # Previously `a or b and c` let the loop run past the array end.
    with pytest.raises(RuntimeError, match="still in flight"):
        ball_flight(altitude=-5000.0)


def test_unreachable_target_altitude_raises():
    # Previously reported a "drop location" in mid-air just after the apex.
    with pytest.raises(RuntimeError, match="never reaches the target altitude"):
        ball_flight(altitude=500.0)


def test_zero_launch_speed_raises():
    # Previously produced NaN results from a 0/0 unit vector.
    with pytest.raises(RuntimeError, match="Launch speed must be positive"):
        ball_flight(v_ball=0.0)
