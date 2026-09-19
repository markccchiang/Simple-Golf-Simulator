#
# Bookkeeping for the main panel's four steps (no Tk here, so it can be tested on its own):
# which steps have run, which results are stale after an input changed, and which in-between
# values the user typed by hand instead of letting a step compute them.
#
import re

STEP_LABELS = ('Optimize wrist torque', 'Simulate swing', 'Launch conditions', 'Ball flight')

STEP_BUTTONS = ('Optimize', 'Swing', 'Launch', 'Ball flight') # short enough for a button

STEP_ACTIVITY = ('Optimizing the wrist-cock torque…', 'Simulating the swing…',
                 'Computing the launch speed and angle…', 'Simulating the ball flight…')

#
# In-between values: the step that computes each one. Typing one by hand makes that step skip.
#
AUTO_FIELDS = {'Q_beta': 0, 'ball_U': 2, 'ball_theta': 2}

#
# The step states
#
IDLE    = 'idle'    # not run yet
DONE    = 'done'    # up to date
STALE   = 'stale'   # an input it uses changed after it ran
MANUAL  = 'manual'  # skipped: its outputs were typed by hand

class Workflow:
    def __init__(self):
        self.states = [IDLE] * 4
        self.manual = set()
        self.computed = {}
        self.before_manual = {} # step -> its state before its outputs were typed by hand

    def input_changed(self, stage):
        """An input used from step `stage` (1-4) on changed: that step and later ones are stale."""
        for i in range(stage - 1, 4):
            if self.states[i] in (DONE, MANUAL):
                self.states[i] = STALE

    def auto_field_edited(self, key, stage):
        """The user typed an in-between value: use it from now on instead of computing it."""
        self.manual.add(key)
        self.input_changed(stage)
        step = AUTO_FIELDS[key]
        if self.skips(step) and self.states[step] != MANUAL:
            self.before_manual[step] = self.states[step]
            self.states[step] = MANUAL

    def use_computed(self, key, stage):
        """Go back to computing an in-between value; returns the value to show ('' if none yet)."""
        self.manual.discard(key)
        self.input_changed(stage)
        step = AUTO_FIELDS[key]
        if self.states[step] == MANUAL:
            # no input changed since (that would have made it stale): its earlier result still holds
            self.states[step] = self.before_manual.get(step, IDLE)
        if key not in self.computed:
            self.states[step] = IDLE
        return self.computed.get(key, '')

    def plan(self, upto):
        """Steps to run so that step `upto` (0-3) and everything it depends on are up to date."""
        return [i for i in range(upto + 1) if self.states[i] != DONE]

    def skips(self, i):
        """True when every value step i computes was typed by hand."""
        keys = [k for k, s in AUTO_FIELDS.items() if s == i]
        return bool(keys) and all(k in self.manual for k in keys)

    def finished(self, i, outputs):
        self.states[i] = DONE
        self.computed.update(outputs)

    def skipped(self, i):
        self.states[i] = MANUAL

    def reset(self):
        self.__init__()

    def status(self):
        """The line under the step buttons, and its kind ('info', 'ok' or 'stale')."""
        if STALE in self.states:
            return 'Inputs changed since the last run, so the affected results are marked stale. Run again to update them.', 'stale'
        if all(s in (DONE, MANUAL) for s in self.states):
            return 'All results are up to date.', 'ok'
        return 'Ready. Click "Run all steps", or click a step to run it and anything it depends on.', 'info'

def check_inputs(values, numeric_keys):
    """Problems with the inputs, as {key: message}. values: the text of every input field."""
    errors = {}
    for key in numeric_keys:
        text = values[key].strip()
        if key in AUTO_FIELDS and text in ('', 'N/A'):
            continue # left for its step to compute
        if _num(text) is None:
            errors[key] = 'Enter a number.'
    def value(key):
        return None if key in errors else _num(values[key])
    R_S, R_A = value('R_S'), value('R_A')
    if None not in (R_S, R_A) and not 0.0 < R_S < R_A:
        errors['R_S'] = 'Must be greater than 0 and smaller than the arm length (4).'
    start, theta = value('set_theta'), value('theta')
    if None not in (start, theta) and start > theta:
        errors['set_theta'] = 'Must not exceed the initial arm angle (10).'
    low, high = value('Q_beta_min'), value('Q_beta_max')
    if None not in (low, high) and low > high:
        errors['Q_beta_min'] = 'Must not exceed the highest torque to try (23).'
    return errors

def _num(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None

def _minus(text):
    """Typeset negative numbers with a true minus sign ('-20.62' -> '−20.62')."""
    return re.sub(r'-(?=\d)', '\u2212', text)

def _plus_minus(bracket):
    """'[-0.22, 2.22]' (the change for Q_beta +/- 0.01 N-m) -> '2.22', the larger of the two."""
    parts = [_num(p) for p in str(bracket).strip('[] ').split(',')]
    if len(parts) != 2 or None in parts:
        return None
    return '%.2f' % max(abs(parts[0]), abs(parts[1]))

def result_cards(v, wf):
    """Text for the results cards from the result values (strings keyed like `entries`).
    Each card: (label, value, detail, state), state being 'none', 'ok' or 'stale'."""
    def card(label, step, value, detail, ready, hint):
        # step: the step whose result this is (None for a value typed by hand, which is never stale)
        if not ready:
            return (label, '—', hint, 'none')
        value, detail = _minus(value), _minus(detail)
        return (label, value, detail, 'stale' if step is not None and wf.states[step] == STALE else 'ok')

    cards = []
    q = _num(v['Q_beta'])
    by_hand = 'Q_beta' in wf.manual
    cards.append(card('Wrist-cock torque', None if by_hand else 0, '%.2f N·m' % q if q is not None else '',
                      'entered by hand' if by_hand else 'found by the optimizer',
                      q is not None and (by_hand or wf.states[0] != IDLE), 'Run step 1, or type item 19'))

    vc, e = _num(v['VC']), _plus_minus(v['error_VC'])
    cards.append(card('Clubhead speed at impact', 1, '%.2f m/s' % vc if vc is not None else '',
                      '%.1f mph' % (vc * 2.23694) + (' · ±%s m/s' % e if e else '') if vc is not None else '',
                      vc is not None, 'Run step 2'))

    ang, e = _num(v['VC_angle']), _plus_minus(v['error_VC_angle'])
    cards.append(card('Clubhead angle at impact', 1, '%.2f°' % ang if ang is not None else '',
                      '±%s° for ±0.01 N·m wrist torque' % e if e else '', ang is not None, 'Run step 2'))

    u, th = _num(v['ball_U']), _num(v['ball_theta'])
    launch_by_hand = {'ball_U', 'ball_theta'} & wf.manual
    cards.append(card('Launch', None if len(launch_by_hand) == 2 else 2, '%.1f m/s @ %.1f°' % (u, th) if None not in (u, th) else '',
                      '%.1f mph' % (u * 2.23694) + (' · entered by hand' if launch_by_hand else '') if u is not None else '',
                      None not in (u, th), 'Run step 3, or type items 40–41'))

    d, lat = _num(v['Distance']), _num(v['Y_final'])
    cards.append(card('Carry distance', 3, '%.1f m' % d if d is not None else '',
                      '%.1f yd' % (d * 1.09361) + (' · lateral %.1f m' % abs(lat) if lat is not None else '') if d is not None else '',
                      d is not None, 'Run step 4'))

    apex, t = _num(v['Apex']), _num(v['Flight_time'])
    cards.append(card('Apex · flight time', 3, '%.1f m · %.2f s' % (apex, t) if None not in (apex, t) else '',
                      '%.0f ft apex' % (apex * 3.28084) if apex is not None else '', None not in (apex, t), 'Run step 4'))
    return cards
