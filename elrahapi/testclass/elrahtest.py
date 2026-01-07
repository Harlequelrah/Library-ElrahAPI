from datetime import datetime

class ElrahTest:


    @classmethod
    def exclude_dates_from_dict(cls, data_dict: dict) -> dict:
        keys_to_exclude = ["date_created", "date_updated","date_deleted"]
        return {
            key: value
            for key, value in data_dict.items()
            if key not in keys_to_exclude
        }

    @classmethod
    def _add_token_to_headers(cls, token: dict, token_type: str) -> dict:
        return {
            "Authorization": f"Bearer {token[token_type]}",
        }

    @classmethod
    def _update_expected_value(cls, expected_value: dict) -> dict:
        current_date = datetime.now().replace(microsecond=0).isoformat()
        expected_value.update(
            {
                "date_created": current_date,
                "date_updated": current_date,
            }
        )
        return expected_value
