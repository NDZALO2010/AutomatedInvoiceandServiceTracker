from decimal import Decimal

from app.services.billing import calculate_client_total


def test_tc_calc_01_boundary_quantities(db_session, seeded_data):
    client_obj = seeded_data["client"]
    service = client_obj.services[0]

    service.quantity = 0
    db_session.commit()
    assert calculate_client_total(db_session, client_obj.client_id) == Decimal("0.00")

    service.quantity = 9999
    db_session.commit()
    assert calculate_client_total(db_session, client_obj.client_id) == Decimal("124987.50")
