USAGE = {}

LIMITS = {
    "free": 100,
    "pro": 1000
}

def check_limit(api_key: str, plan: str):
    if api_key not in USAGE:
        USAGE[api_key] = 0

    USAGE[api_key] += 1

    used = USAGE[api_key]
    limit = LIMITS[plan]

    if used > limit:
        return False, used, limit

    return True, used, limit
