from app.constants import (
    ORDER_CANCELLED,
    ORDER_DELIVERED,
    ORDER_PENDING,
    ORDER_PROCESSING,
    ORDER_SHIPPED,
)


def get_order_status_label(status, lang="ar"):
    labels = {
        "ar": {
            ORDER_PENDING: "قيد المراجعة",
            ORDER_PROCESSING: "قيد التجهيز",
            ORDER_SHIPPED: "تم الشحن",
            ORDER_DELIVERED: "تم التسليم",
            ORDER_CANCELLED: "ملغي",
        },
        "en": {
            ORDER_PENDING: "Pending",
            ORDER_PROCESSING: "Processing",
            ORDER_SHIPPED: "Shipped",
            ORDER_DELIVERED: "Delivered",
            ORDER_CANCELLED: "Cancelled",
        },
        "ja": {
            ORDER_PENDING: "保留中",
            ORDER_PROCESSING: "処理中",
            ORDER_SHIPPED: "発送済み",
            ORDER_DELIVERED: "配達済み",
            ORDER_CANCELLED: "キャンセル済み",
        },
    }

    return labels.get(lang, labels["ar"]).get(status, status)


def get_order_timeline(order, lang="ar"):
    status = order.status

    steps = [
        {
            "key": ORDER_PENDING,
            "icon": "🧾",
            "title": {
                "ar": "تم إنشاء الطلب",
                "en": "Order created",
                "ja": "注文が作成されました",
            },
        },
        {
            "key": ORDER_PROCESSING,
            "icon": "⚙️",
            "title": {
                "ar": "قيد التجهيز",
                "en": "Processing",
                "ja": "処理中",
            },
        },
        {
            "key": ORDER_SHIPPED,
            "icon": "🚚",
            "title": {
                "ar": "تم الشحن",
                "en": "Shipped",
                "ja": "発送済み",
            },
        },
        {
            "key": ORDER_DELIVERED,
            "icon": "📦",
            "title": {
                "ar": "تم التسليم",
                "en": "Delivered",
                "ja": "配達済み",
            },
        },
    ]

    if status == ORDER_CANCELLED:
        return [
            {
                "key": ORDER_PENDING,
                "icon": "🧾",
                "title": {
                    "ar": "تم إنشاء الطلب",
                    "en": "Order created",
                    "ja": "注文が作成されました",
                }.get(lang, "تم إنشاء الطلب"),
                "done": True,
                "active": False,
            },
            {
                "key": ORDER_CANCELLED,
                "icon": "❌",
                "title": {
                    "ar": "تم إلغاء الطلب",
                    "en": "Order cancelled",
                    "ja": "注文がキャンセルされました",
                }.get(lang, "تم إلغاء الطلب"),
                "done": True,
                "active": True,
            },
        ]

    order_keys = [
        ORDER_PENDING,
        ORDER_PROCESSING,
        ORDER_SHIPPED,
        ORDER_DELIVERED,
    ]

    current_index = order_keys.index(status) if status in order_keys else 0

    timeline = []

    for index, step in enumerate(steps):
        timeline.append({
            "key": step["key"],
            "icon": step["icon"],
            "title": step["title"].get(lang, step["title"]["ar"]),
            "done": index <= current_index,
            "active": index == current_index,
        })

    return timeline