import os


def get_update_frequency_sec():
    env = os.getenv("NEWS_API_UPDATE_FREQUENCY_SEC", 300)
    check_not_null(env, "NewsAPI update frequency not defined")
    return int(env)


def get_language():
    env = os.getenv("NEWS_API_LANGUAGE", "ru")
    check_not_null(env, "NewsAPI language not defined")
    return env


def get_api_key():
    env = os.getenv("NEWS_API_KEY")
    check_not_null(env, "NewsAPI key not defined")
    return env


def get_sources():
    env = os.getenv("NEWS_API_SOURCES")
    check_not_null(env, "NewsAPI sources not defined")
    return env


################################################################################


def check_not_null(env, error_message):
    if not env:
        raise RuntimeError(error_message)


def get_comma_separated_list(line):
    arr = line.strip().split(",")
    if not arr:
        raise RuntimeError("Cannot parse comma separated list: " + str(line))
    return arr
