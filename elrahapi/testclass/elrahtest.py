from datetime import datetime

class ElrahTest:

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
