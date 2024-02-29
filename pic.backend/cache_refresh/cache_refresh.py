from common_component.src.component.services.cache_service import cache_manage_service

from common_component.src.core.helpers.ssm_helper import get_ssm_parameter
from common_component.src.core.utils.Logger import Log
import service
import time


log = Log().get_logger_service()

key_func_mapping_reference_service = {
    "facility_types_list": "get_facility_types",
    "brands_list": "get_brands",
    "cities_list": "get_cities",
    "language_list": "get_language",
    "province_list": "get_province",
    "status_list": "get_status",
    "time_zones_list": "get_all_time_zones",
    "all_products": "get_all_products",
    "notification_types": "get_notification_types",
    "contact_types_list": "get_contact_types",
    "base_product_list": "get_base_products",
    "follow_action_status_list": "get_tactic_follow_action_status",
    "follow_movement_list": "get_tactic_follow_movement"
}


def refresh_cache_data(event, key):
    if event == "TWELVE-HOURS":
        try:
            key_names = get_ssm_parameter('/pic/cache/refresh_time/key_names_for_reference_service').split(',')

            if key in key_names:
                function_name = key_func_mapping_reference_service[key]
                push_cache_data(key, 'EN', function_name)
                push_cache_data(key, 'FR', function_name)
        except Exception as exc:
            log.debug("Exception occurred while pushing data to memcached")

    elif event == "FOUR-HOURS":
        try:
            refresh_data('EN')
            refresh_data('FR')
            return "Outlet data pushed to memcached"
        except Exception as exc:
            log.debug("Exception occurred while pushing outlet selector data to memcached")


def refresh_data(lang):
    refresh_time = get_ssm_parameter('/pic/cache/refresh_time/station_master')

    cache_key = 'outlet_selector_list_' + lang.lower()
    remove_key_from_cache(cache_key)
    response_data = service.get_outlet_selector('', lang)
    value = response_data['data']['outlet_selector_list']
    if value:
        response = cache_manage_service.set_cached_data(cache_key, value,
                                                        int(refresh_time))  # push db output to cache for EN
        time.sleep(1)
        log_response(response, cache_key)


def push_cache_data(key, lang, function_name):
    refresh_time = get_ssm_parameter('/pic/cache/refresh_time/station_master')

    cache_key = key + '_' + lang.lower()
    remove_key_from_cache(cache_key)
    func = getattr(service, function_name)
    response_data = func(lang)
    value = response_data['data'][key]

    if value:
        response = cache_manage_service.set_cached_data(cache_key, value,
                                                        int(refresh_time))  # push db output to cache for EN

        log_response(response, cache_key)


def remove_key_from_cache(key):
    response = cache_manage_service.delete_cache_key(key)
    log.info("Cached removed for the given key. key: %s", key)


def log_response(response, key):
    if response:
        log.info("Data cached for the given key. key: %s", key)
    else:
        log.debug("Something went wrong while pushing the data to memcached for. key: %s", key)


def refresh_cities_data(event, city_key):
    if event == "TWELVE-HOURS":
        try:
            key_names = get_ssm_parameter('/pic/cache/refresh_time/key_names_for_reference_service').split(',')

            if city_key in key_names:
                refresh_time = get_ssm_parameter('/pic/cache/refresh_time/station_master')

                # English lang
                lang = 'EN'
                response_data = service.get_province(lang)
                value = response_data['data']["province_list"]
                for province in value:
                    key = 'ca_cities_' + str(province['id']) + '_' + lang.lower()
                    remove_key_from_cache(key)
                    response_data = service.get_cities(province['id'], lang)
                    time.sleep(1)
                    response = cache_manage_service.set_cached_data(key, response_data['data']['cities_list'], int(refresh_time))
                    log_response(response, key)

                # FR lang
                lang = 'FR'
                for province in value:
                    key = 'ca_cities_' + str(province['id']) + '_' + lang.lower()
                    remove_key_from_cache(key)
                    response_data = service.get_cities(province['id'], lang)
                    time.sleep(1)
                    response = cache_manage_service.set_cached_data(key, response_data['data']['cities_list'],
                                                                    int(refresh_time))
                    log_response(response, key)

        except Exception as exc:
            log.debug("Exception occurred while pushing cities data to memcached")


def refresh_marketer_data():
    refresh_time = get_ssm_parameter('/pic/cache/refresh_time/station_master')
    key = "marketers_list"
    remove_key_from_cache(key)
    response_data = service.get_marketer()
    value = response_data['data'][key]
    if value:
        response = cache_manage_service.set_cached_data(key, value,
                                                        int(refresh_time))
        log_response(response, key)


