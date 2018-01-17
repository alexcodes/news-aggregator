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


def get_storage_filename():
    env = os.getenv("NEWS_STORAGE_FILENAME", "storage.csv")
    check_not_null(env, "News storage not defined")
    return env


def get_article_ttl_hours():
    env = os.getenv("NEWS_ARTICLE_TTL_HOURS", 24)
    check_not_null(env, "News article ttl not defined")
    return int(env)


def get_default_image_filename():
    env = os.getenv("IMAGE_DEFAULT_FILENAME")
    check_not_null(env, "Default image filename not defined")
    return env


def get_image_storage_path():
    env = os.getenv("IMAGE_STORAGE_PATH", "./images/")
    check_not_null(env, "Image storage path not defined")
    return env


def get_image_font_filename():
    env = os.getenv("IMAGE_FONT_FILENAME")
    check_not_null(env, "Image font filename not defined")
    return env


def get_vk_access_token():
    env = os.getenv("VK_ACCESS_TOKEN")
    check_not_null(env, "VK access token not defined")
    return env


def get_vk_target_group():
    env = os.getenv("VK_TARGET_GROUP")
    check_not_null(env, "VK target group not defined")
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
