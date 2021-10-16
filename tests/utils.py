from typing import Dict


def make_expect_result(params, reg_time, idx) -> Dict:
    expected = {
        'price': params['price'], 'registrant': 'Auth_User', 'reg_date': reg_time, 'idx': idx,
        'fee': None,
        'confirmed_editor': None, 'updater': None, 'update_date': None,
        'KO': {
            'item_idx': idx, 'language': 0, 'title': params['title'], 'content': params['content'], 'idx': idx
        }
    }
    return expected


def make_change_history_info(change_infos, reg_date, idx, p_item_idx) -> Dict:
    result = {
        "item_idx": p_item_idx,
        "registrant": "Auth_User",
        "reg_date": reg_date,
        "idx": idx,
        "title": None,
        "content": None,
        "price": None,
        "fee": None,
        "confirmed_editor": None,
        "confirmed_date": None
    }

    for key, value in change_infos.items():
        result[key] = value

    return result
