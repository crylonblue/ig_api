API_URL = "https://i.instagram.com/api/v1/"
API_URL_V2 = "https://i.instagram.com/api/v2/"

LOGGING_URL = "https://graph.instagram.com/logging_client_events"

APP_ID = "124024574287414"

APP_VER = "197.0.0.20.119 (305020938)"

USER_AGENT = "Instagram 197.0.0.20.119 (iPhone10,6; iOS 14_4_2; de_DE; de-DE; scale=3.00; 1125x2436; 275424340) AppleWebKit/420+"

BLOKS_VERSION = "29d3248efc1cfc10a0dbafd84eb58fd7eebc6b99e626c5bfa0fe615b8ff784d9"


BATCH_QUERY = "Query IGQPQuery: Viewer {\n    viewer() {\n        eligible_promotions.ig_parameters(<ig_parameters>).surface_nux_id(<surface>).external_gating_permitted_qps(<external_gating_permitted_qps>).include_holdouts(true).trigger_name(<trigger_name>).supports_client_filters(true).trigger_context_v2(<trigger_context_v2>) {\n            edges {\n                log_eligibility_waterfall,\n                is_holdout,\n                priority,\n                time_range {\n                    start,\n                    end\n                },\n                node {\n                    id,\n                    promotion_id,\n                    logging_data,\n                    max_impressions,\n                    triggers,\n                    template {\n                        name,\n                        parameters {\n                          name,\n                          required,\n                          string_value,\n                          bool_value,\n                          color_value\n                        }\n                    },\n                    contextual_filters {\n                        clause_type,\n                        filters {\n                            filter_type,\n                            passes_if_not_supported,\n                            unknown_action,\n                            value {\n                                name,\n                                required,\n                                bool_value,\n                                int_value,\n                                string_value\n                            },\n                            extra_datas {\n                                name,\n                                required,\n                                bool_value,\n                                int_value,\n                                string_value\n                            }\n                        },\n                        clauses {\n                            clause_type,\n                            filters {\n                                filter_type,\n                                passes_if_not_supported,\n                                unknown_action,\n                                value {\n                                    name,\n                                    required,\n                                    bool_value,\n                                    int_value,\n                                    string_value\n                                },\n                                extra_datas {\n                                    name,\n                                    required,\n                                    bool_value,\n                                    int_value,\n                                    string_value\n                                }\n                            },\n                            clauses {\n                                clause_type,\n                                filters {\n                                    filter_type,\n                                    passes_if_not_supported,\n                                    unknown_action,\n                                    value {\n                                        name,\n                                        required,\n                                        bool_value,\n                                        int_value,\n                                        string_value\n                                    },\n                                    extra_datas {\n                                        name,\n                                        required,\n                                        bool_value,\n                                        int_value,\n                                        string_value\n                                    }\n                                }\n                            }\n                        }\n                    },\n                    creatives {\n                      title {\n                        text\n                      },\n                      content {\n                        text\n                      },\n                      footer {\n                        text,\n                        aggregated_ranges {\n                            count,\n                            length,\n                            offset\n                        },\n                        ranges {\n                            entity_is_weak_reference,\n                            length,\n                            offset,\n                            override_uri,\n                            entity {\n                                url\n                            }\n                        }\n                      },\n                      social_context {\n                        text\n                      },\n                      social_context_images,\n                      primary_action{\n                        title {\n                          text\n                        },\n                        url,\n                        limit,\n                        dismiss_promotion\n                      },\n                      secondary_action {\n                        title {\n                          text\n                        },\n                        url,\n                        limit,\n                        dismiss_promotion\n                      },\n                      dismiss_action{\n                        title {\n                          text\n                        },\n                        url,\n                        limit,\n                        dismiss_promotion\n                      },\n                      image.scale(<scale>) {\n                        uri,\n                        width,\n                        height\n                      },\n                      dark_mode_image.scale(<scale>) {\n                        uri,\n                        width,\n                        height\n                      }\n                    },\n                    is_server_force_pass\n                }\n            }\n        }\n    }\n}\n"

BATCHES = [
    {
        "id": "4669",
        "triggers": [["instagram_inbox_header"], ["instagram_other_logged_in_user_id_loaded"], ["instagram_profile_page"], ["instagram_other_profile_page_header"], ["instagram_other_profile_page_header"]]
    },
    {
        "id": "8971",
        "triggers": [["instagram_self_profile_floating_banner_prompt"]]
    },
    {
        "id": "5736",
        "triggers": [["instagram_explore_prompt"],["instagram_profile_page_prompt"],["instagram_other_profile_page_prompt"]]
    },
    {
        "id": "5829",
        "triggers": [["instagram_profile_promotions_cta_tooltip", "instagram_self_profile_tooltip"], ["instagram_other_checkout_profile_tooltip", "instagram_other_profile_tooltip"],["instagram_explore_tooltip"]]
    }
]

HEADERS = {
    "priority": "u=2, i",
    "ig-intended-user-id": "0",
    "x-ig-connection-speed": "3kbps",
    #"x-ig-device-id": "E5592027-D411-4C9C-8943-777069389330",
    "x-ig-app-startup-country": "unknown",
    "x-ig-capabilities":  "36r/Fx8=",
    #"x-pigeon-rawclienttime": "1626967292.90395",
    "x-ig-device-locale": "de-DE",
    "x-ig-abr-connection-speed-kbps": "0",
    "accept-language": "de-DE;q=1.0",
    "user-agent": USER_AGENT,
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "x-ig-app-locale": "de",
    "x-ig-bandwidth-speed-kbps": "0.000",
    "x-ig-mapped-locale": "de_DE",
    "x-ig-www-claim": "0",
    #"x-mid": "YPgzUwAAAAGqbPZDdG5DILY5S-Dc",
    "x-bloks-is-panorama-enabled": "true",
    "x-bloks-version-id": BLOKS_VERSION,
    #"x-pigeon-session-id": "1B8AE061-D4ED-4957-9FC2-6970A6AC8D83",
    "x-ig-app-id": APP_ID,
    "x-ig-connection-type": "WiFi",
    "x-tigon-is-retry": "False",
    "accept-encoding": "zstd, gzip, deflate",
    "x-fb-http-engine": "Liger",
    "x-fb-client-ip": "True",
    "x-fb-server-cluster": "True"
}


ACCESS_TOKEN = "84a456d620314b6e92a16d8ff1c792dc"

SUPPORTED_CAPABILITIES = [
    {
        "name": "hair_segmentation",
        "value": "hair_segmentation_enabled"
    },
    {
        "name": "body_tracking",
        "value": "body_tracking_enabled"
    },
    {
        "name": "GYROSCOPE",
        "value": "GYROSCOPE_ENABLED"
    },
    {
        "name": "HALF_FLOAT_RENDER_PASS",
        "value": "HALF_FLOAT_RENDER_PASS_ENABLED"
    }, 
    {
        "name": "VERTEX_TEXTURE_FETCH",
        "value": "VERTEX_TEXTURE_FETCH_ENABLED"
    },
    {
        "name": "DEPTH_SHADER_READ",
        "value": "DEPTH_SHADER_READ_ENABLED"
    },
    {
        "name": "MULTIPLE_RENDER_TARGETS",
        "value": "MULTIPLE_RENDER_TARGETS_ENABLED"
    },
    {
        "name": "SUPPORTED_SDK_VERSIONS",
        "value": "73.0,74.0,75.0,76.0,77.0,78.0,79.0,80.0,81.0,82.0,83.0,84.0,85.0,86.0,87.0,88.0,89.0,90.0,91.0,92.0,93.0,94.0,95.0,96.0,97.0,98.0,99.0,100.0,101.0,102.0,103.0,104.0,105.0,106.0,107.0,108.0"
    },
    {
        "name": "COMPRESSION",
        "value": "PVR_COMPRESSION"
    },
    {
        "name": "FACE_TRACKER_VERSION",
        "value":"14"
    }]