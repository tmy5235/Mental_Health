"""Narrow fixed replies, not a distress detector or clinical assessment.

Phrase matching can miss indirect wording and match quoted/negated statements.
The bundled support control is always available, independent of these rules.
"""

def reviewed_reply(question):
    text = ' '.join(question.casefold().replace('’', "'").split())
    if any(term in text for term in ('suicid', 'kill myself', 'hurt myself', 'self-harm', 'self harm', 'end my life')):
        return ('This coursework app cannot provide crisis care. '
                'Open Crisis support for external help. No one monitors this app.')
    history_question = any(term in text for term in ('session', 'history', 'last practice', 'did i', 'was my'))
    if history_question and any(term in text for term in ('paus', 'uninterrupted', 'without a break')):
        return ('Saved session records do not include pause events, so this app cannot tell '
                'whether a past session was paused. Completion and active duration do not '
                'establish an uninterrupted session.')
    return None
