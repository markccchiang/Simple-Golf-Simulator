import Workflow
from Workflow import DONE, IDLE, MANUAL, STALE, Workflow as Flow


def run_all(wf, outputs=None):
    for i in wf.plan(3):
        if wf.skips(i):
            wf.skipped(i)
        else:
            wf.finished(i, (outputs or {}).get(i, {}))


def test_plan_runs_missing_earlier_steps_first():
    wf = Flow()
    assert wf.plan(2) == [0, 1, 2]
    wf.finished(0, {})
    assert wf.plan(2) == [1, 2]


def test_changing_an_input_marks_its_step_and_later_ones_stale():
    wf = Flow()
    run_all(wf)
    wf.input_changed(3)  # e.g. ball mass, used from the launch step on
    assert wf.states == [DONE, DONE, STALE, STALE]
    assert wf.plan(3) == [2, 3]


def test_steps_that_never_ran_stay_idle_when_an_input_changes():
    wf = Flow()
    wf.finished(0, {})
    wf.input_changed(1)
    assert wf.states == [STALE, IDLE, IDLE, IDLE]


def test_a_hand_typed_wrist_torque_skips_the_optimizer():
    wf = Flow()
    wf.auto_field_edited('Q_beta', 2)
    run_all(wf)
    assert wf.states == [MANUAL, DONE, DONE, DONE]


def test_typing_the_torque_after_a_run_shows_the_optimizer_as_skipped():
    wf = Flow()
    run_all(wf)
    wf.auto_field_edited('Q_beta', 2)
    assert wf.states == [MANUAL, STALE, STALE, STALE]


def test_after_an_input_change_going_back_to_computing_reruns_the_optimizer():
    wf = Flow()
    run_all(wf, {0: {'Q_beta': '-20.62'}})
    wf.auto_field_edited('Q_beta', 2)
    wf.input_changed(1)  # e.g. arm torque
    wf.use_computed('Q_beta', 2)
    assert wf.plan(3) == [0, 1, 2, 3]


def test_the_launch_step_is_skipped_only_when_both_launch_values_are_typed():
    wf = Flow()
    wf.auto_field_edited('ball_U', 4)
    assert not wf.skips(2)
    wf.auto_field_edited('ball_theta', 4)
    assert wf.skips(2)


def test_going_back_to_the_computed_value_restores_it_and_reruns_later_steps():
    wf = Flow()
    run_all(wf, {0: {'Q_beta': '-20.62'}})
    wf.auto_field_edited('Q_beta', 2)
    assert wf.use_computed('Q_beta', 2) == '-20.62'
    assert 'Q_beta' not in wf.manual
    assert wf.plan(3) == [1, 2, 3]  # the optimizer's result is still valid; only later steps rerun


def test_going_back_to_computing_before_the_step_ever_ran_leaves_it_to_run():
    wf = Flow()
    wf.auto_field_edited('Q_beta', 2)
    run_all(wf)
    assert wf.use_computed('Q_beta', 2) == ''
    assert wf.states[0] == IDLE


def test_status_line():
    wf = Flow()
    assert wf.status()[1] == 'info'
    run_all(wf)
    assert wf.status()[1] == 'ok'
    wf.input_changed(4)
    assert wf.status()[1] == 'stale'


RESULTS = dict(Q_beta='-20.62', VC='52.76', error_VC='[-0.01, 0.00]', VC_angle='-0.11',
               error_VC_angle='[-0.25, 0.25]', ball_U='76.20', ball_theta='14.89',
               Distance='201.088', Y_final='-0.000', Apex='24.30', Flight_time='5.16')


def test_result_cards_show_values_units_and_error_bars():
    wf = Flow()
    run_all(wf)
    cards = {c[0]: c for c in Workflow.result_cards(RESULTS, wf)}
    assert cards['Clubhead speed at impact'][1:] == ('52.76 m/s', '118.0 mph · ±0.01 m/s', 'ok')
    assert cards['Clubhead angle at impact'][2] == '±0.25° for ±0.01 N·m wrist torque'
    assert cards['Launch'][1] == '76.2 m/s @ 14.9°'
    assert cards['Carry distance'][1:3] == ('201.1 m', '219.9 yd · lateral 0.0 m')
    assert cards['Apex · flight time'][1:3] == ('24.3 m · 5.16 s', '80 ft apex')


def test_result_cards_mark_stale_results_and_hide_missing_ones():
    wf = Flow()
    run_all(wf)
    wf.input_changed(4)
    empty = dict(RESULTS, Distance='N/A', Y_final='N/A')
    cards = {c[0]: c for c in Workflow.result_cards(empty, wf)}
    assert cards['Clubhead speed at impact'][3] == 'ok'
    assert cards['Apex · flight time'][3] == 'stale'
    assert cards['Carry distance'][1:] == ('—', '', 'none')


def test_hand_typed_values_are_never_stale():
    wf = Flow()
    wf.auto_field_edited('Q_beta', 2)
    run_all(wf)
    wf.input_changed(1)
    cards = {c[0]: c for c in Workflow.result_cards(RESULTS, wf)}
    assert cards['Wrist-cock torque'][2:] == ('entered by hand', 'ok')
