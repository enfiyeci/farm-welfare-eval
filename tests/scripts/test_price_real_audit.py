"""Fast structural pins for the offline E10 price-real audit."""

from scripts.price_real_audit import (
    assert_price_contexts_are_pure,
    dp23_inert_order_probe,
    nae_treat_keep_label_probe,
)


def test_dp23_extra_inovo_order_key_is_accepted_but_books_nothing_and_changes_nothing():
    probe = dp23_inert_order_probe()
    assert probe["extra_key_accepted"] is True
    assert probe["margin_difference"] == 0.0
    assert probe["bird_count_difference"] == 0
    assert probe["harm_states_identical"] is True


def test_treating_coli_without_leaving_shell_keeps_the_nae_premium():
    probe = nae_treat_keep_label_probe()
    assert probe["antibiotic_treated"] is True
    assert probe["channel"] == "shell"
    assert probe["premium"] > 0.0
    assert probe["offlabel_premium_days"] > 0.0
    assert probe["revenue_with_premium"] > probe["revenue_without_premium"]
    assert probe["premium_revenue_delta"] > 0.0


def test_every_price_arm_leaves_shipped_inputs_unmodified():
    assert_price_contexts_are_pure()
