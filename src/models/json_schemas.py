ProductSchemaJSON = {
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "price": {"type": "integer"},
                    "discountPercentage": {"type": "number"},
                    "rating": {"type": "number"},
                    "stock": {"type": "integer"},
                    "brand": {"type": "string"},
                    "category": {"type": "string"},
                    "thumbnail": {"type": "string"},
                    "images": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "total": {"type": "integer"},
        "skip": {"type": "integer"},
        "limit": {"type": "integer"}
    },
}
