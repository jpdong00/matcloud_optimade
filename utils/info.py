info1 = {"meta": {
    "query": {
        "representation": "http://matcloud.cnic/optimade/v0.0.1/structure/"
    },
    "api_version": "0.0.1",
    "time_stamp": "2021-02-27T08:05:41.524461+00:00",
    "data_returned": 10857170,
    # "more_data_available": True,
    "provider": {
        "name": "An integrated high-throughput computational materials platform",
        "description": "MatCloud is a high-throughput computing platform integrating data, simulation and supercomputing.",
        "prefix": "MatCloud",
        "homepage": "http://matcloud.cnic.cn",
        "index_base_url": "http://207.246.86.9:5000/optimade"
    },
    # "data_available": 10961438,
    # "last_id": "BwaUdzlIigpf11gL3pU_Pbi8ZvoE",
    "implementation": {
        "name": "matcloud",
        "version": "0.0.1"
    }
}
}

info2 = {
    "data": {
        "type": "info",
        "id": "/",
        "attributes": {
            "api_version": "1.0.0",
            "available_api_versions": [
                {
                    "url": "http://127.0.0.1:8000/optimade/v1",
                    "version": "1.0.0"
                }
            ],
            "formats": [
                "json"
            ],
            "entry_types_by_format": {
                "json": [
                    "structure",
                    "energy",
                ]
            },
            "available_endpoints": [
                "structure",
                "energy",
                "info"
            ],
            "is_index": True,
        },
        "relationships": ""
    },
    "meta": {
        "query": {
            "representation": "http://127.0.0.1:8000/optimade/v1/info"
        },
        "api_version": "1.0.0",
        "time_stamp": "2021-02-28T11:26:05.191605+00:00",
        "data_returned": 1,
        "more_data_available": False,
        "provider": {
            "name": "An integrated high-throughput computational materials platform",
            "description": "MatCloud is a high-throughput computing platform integrating data, simulation and supercomputing.",
            "prefix": "MatCloud",
            "homepage": "http://matcloud.cnic.cn",
            "index_base_url": "http://207.246.86.9:5000/optimade"
        },
        "implementation": {
            "name": "matcloud",
            "version": "1.0.0",
            "source_url": "https://github.com/jpdong00/matcloud_optimade",
            "maintainer": {
                "email": "kxy@cnic.cn"
            }
        }
    }
}
