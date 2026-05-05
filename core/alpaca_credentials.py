from __future__ import annotations

import os
from typing import cast


_PROFILE_TO_ENV = {
    "v1": ("V1_APCA_API_KEY_ID", "V1_APCA_API_SECRET_KEY"),
    "v2": ("V2_APCA_API_KEY_ID", "V2_APCA_API_SECRET_KEY"),
}


def resolve_alpaca_credentials(profile: str) -> tuple[str, str]:
    """Resolve Alpaca API credentials for a named profile.

    Supported profiles are:
    - v1 -> V1_APCA_API_KEY_ID / V1_APCA_API_SECRET_KEY
    - v2 -> V2_APCA_API_KEY_ID / V2_APCA_API_SECRET_KEY
    """
    normalized_profile = profile.strip().lower()
    if normalized_profile not in _PROFILE_TO_ENV:
        supported = ", ".join(sorted(_PROFILE_TO_ENV))
        raise ValueError(
            f"Unsupported Alpaca profile '{profile}'. Supported profiles: {supported}."
        )

    api_key_var, secret_key_var = _PROFILE_TO_ENV[normalized_profile]
    api_key = os.environ.get(api_key_var)
    secret_key = os.environ.get(secret_key_var)
    missing = [name for name, value in ((api_key_var, api_key), (secret_key_var, secret_key)) if not value]
    if missing:
        raise EnvironmentError(
            "Missing Alpaca credentials for profile "
            f"'{normalized_profile}'. Missing: {', '.join(missing)}."
        )

    return api_key, secret_key  # type: ignore[return-value]  # guarded by missing-vars check above
