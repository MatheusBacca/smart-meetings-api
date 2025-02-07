ws_responses: dict = {
    "rooms_get": {
        200: {
            "description": "Indicates that the request was successful.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Sala A",
                            "capacity": 4,
                            "location": "Andar 1",
                            "creator_id": 1,
                            "created_at": "2025-02-06T19:32:42",
                        },
                        {
                            "id": 2,
                            "name": "Sala B",
                            "capacity": 8,
                            "location": "Andar 1",
                            "creator_id": 1,
                            "created_at": "2025-02-06T19:33:48",
                        },
                    ]
                }
            },
        },
    },
    "rooms_get_availability": {
        200: {
            "description": "Indicates that the request was successful.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Sala A",
                        "capacity": 4,
                        "location": "Andar 1",
                        "creator_id": 1,
                        "created_at": "2025-02-06T19:32:42",
                    }
                }
            },
        },
        400: {
            "description": "Indicates that there is an error with the request parameters.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "The start time must be earlier than the end time."
                    }
                }
            },
        },
    },
    "rooms_get_reservations": {
        200: {
            "description": "Indicates that the request was successful.",
            "content": {
                "application/json": {
                    "example": {
                        "reservations": [
                            {
                                "id": 1,
                                "user_id": 1,
                                "room_id": 1,
                                "start_time": "2025-02-07T12:45:45",
                                "end_time": "2025-02-07T12:50:50",
                                "created_at": "2025-02-07T09:16:17",
                            }
                        ]
                    }
                }
            },
        },
        404: {
            "description": "Indicates that the searched room was not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Room with id '5' not found."}
                }
            },
        },
    },
    "rooms_post": {
        201: {
            "description": "Indicates that the request was successful.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Sala A",
                        "capacity": 4,
                        "location": "Andar 1",
                        "creator_id": 1,
                        "created_at": "2025-02-06T19:32:42",
                    }
                }
            },
        },
        422: {
            "description": "Indicates that the creator_id is not a valid user id.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with id '5' not found. If you want to create a new user, please use POST /users API to create a new one"
                    }
                }
            },
        },
    },
    "users_get": {
        200: {
            "description": "Indicates that the request was successful.",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "name": "test", "email": "test@gmail.com"},
                        {"id": 2, "name": "tester", "email": "tester@gmail.com"},
                    ]
                }
            },
        },
    },
    "users_post": {
        201: {
            "description": "Indicates that the request was successful.",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "test", "email": "test@gmail.com"}
                }
            },
        },
        409: {
            "description": "Indicates that there is already a registered user with the input name or email.",
            "content": {
                "application/json": {
                    "example": {"detail": "User with name 'tester' already exists."}
                }
            },
        },
    },
    "reservations_get": {
        200: {
            "description": "Indicates that the request was successful.",
            "content": {
                "application/json": {
                    "example": {
                        "reservations": [
                            {
                                "user_id": 1,
                                "room_id": 1,
                                "start_time": "2025-02-07T12:45:45",
                                "end_time": "2025-02-07T12:50:50",
                                "id": 1,
                                "created_at": "2025-02-07T09:16:17",
                            },
                            {
                                "user_id": 1,
                                "room_id": 1,
                                "start_time": "2025-02-07T13:30:00",
                                "end_time": "2025-02-07T13:35:00",
                                "id": 2,
                                "created_at": "2025-02-07T09:28:47",
                            },
                        ]
                    }
                }
            },
        },
    },
    "reservations_post": {
        201: {
            "description": "Indicates that the request was successful.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Sala A",
                        "capacity": 4,
                        "location": "Andar 1",
                        "creator_id": 1,
                        "created_at": "2025-02-06T19:32:42",
                    }
                }
            },
        },
        400: {
            "description": "Indicates that there is an error with the request parameters.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "The start time must be earlier than the end time."
                    }
                }
            },
        },
    },
    "reservations_delete": {
        204: {
            "description": "Indicates that the request was successful.",
        },
    },
}
