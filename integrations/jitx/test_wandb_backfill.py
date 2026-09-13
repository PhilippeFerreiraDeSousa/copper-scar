import unittest
from wandb_backfill import choose_incumbent


def evaluation(opens=313, errors=44, warnings=224, reliable=True, invariants=True):
    return {'evaluation_reliable': reliable, 'invariants_ok': invariants,
            'cost': [0, opens, errors, warnings, 0, 0, 7] if reliable else None,
            'metrics': {'missing_connections': opens, 'physical_errors': errors,
                        'incorrect_connections': 0, 'erc_errors': 0}}


class CorrectedIncumbentTests(unittest.TestCase):
    def test_fewer_opens_cannot_hide_new_physical_errors(self):
        self.assertFalse(choose_incumbent(evaluation(307, 48), evaluation()))

    def test_unreliable_or_changed_circuit_never_becomes_baseline(self):
        self.assertFalse(choose_incumbent(evaluation(reliable=False), None))
        self.assertFalse(choose_incumbent(evaluation(invariants=False), None))

    def test_latest_recheck_reconstructs_incumbent_without_stale_retain_flag(self):
        candidate = evaluation(310, warnings=237)
        candidate['retain'] = False
        self.assertTrue(choose_incumbent(candidate, evaluation()))

    def test_equal_checkpoint_is_not_a_new_incumbent(self):
        self.assertFalse(choose_incumbent(evaluation(), evaluation()))


if __name__ == '__main__':
    unittest.main()
