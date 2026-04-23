from .rules import RULES, NO_MATCH_RESULT


def evaluate_task(task, visits=None):
    if visits is None:
        visits = list(task.visits.select_related('field_agent').all())

    matched = []
    for rule in RULES:
        try:
            if rule['condition'](task, visits):
                matched.append(rule)
        except Exception:
            continue

    if not matched:
        return NO_MATCH_RESULT

    best = matched[0]
    return {
        'rule': best['id'],
        'severity': best['severity'],
        'confidence': best['confidence'],
        'suggestion': best['suggestion'],
        'all_triggered': [r['id'] for r in matched],
    }
