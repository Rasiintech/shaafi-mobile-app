# import frappe
# import time
# from shaafi_mobile_app.utils.image_utils import format_image_url
# from shaafi_mobile_app.utils.response_utils import response_util

# @frappe.whitelist()
# def get_all_banners():
#     try:
#         # 1. Fetch all Doctor banners
#         banners = frappe.get_all(
#             "Doctor banners",
#             fields=["name", "banner_image", "banner_type"]
#         )

#         # Check if banners list is empty
#         if not banners:
#             return response_util(
#                 status="error",
#                 message="No banners found in the system.",
#                 data=None,
#                 http_status_code=404
#             )

#         # 2. Format each banner's image URL using the utility function
#         for banner in banners:
#             banner["banner_image"] = format_image_url(banner.get("banner_image"))

#         # 3. Return the banners data using the response utility
#         return response_util(
#             status="success",
#             message="Banners fetched successfully",
#             data=banners,
#             http_status_code=200
#         )

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Get All Doctor Banners Error")
#         return response_util(
#             status="error",
#             message="An error occurred while fetching doctor banners.",
#             data=None,
#             error=e,
#             http_status_code=500
#         )
import frappe
import time
from frappe.utils import now_datetime
from shaafi_mobile_app.utils.image_utils import format_image_url
from shaafi_mobile_app.utils.response_utils import response_util

@frappe.whitelist()
def get_all_banners():
    start_time = time.time()

    try:
        current_time = now_datetime()

        # Step 1: Fetch all banners
        banners = frappe.get_all(
            "Doctor banners",  # or rename to just "Banners"
            fields=[
                "name",
                "banner_image",
                "banner_type",
                "title",
                "description",
                "details",
                "valid_from",
                "valid_till"
            ],
            order_by="valid_from desc"
        )

        # Step 2: Filter only expired 'Service' banners
        active_banners = []
        for banner in banners:
            if banner["banner_type"] == "Service":
                valid_till = banner.get("valid_till")
                # if not valid_till or valid_till > current_time:
                # Only include if valid_till is present and in the future
                if valid_till and valid_till > current_time:
                    active_banners.append(banner)
            else:
                active_banners.append(banner)

        # Step 3: Format images
        for banner in active_banners:
            banner["banner_image"] = format_image_url(banner.get("banner_image"))

        if not active_banners:
            return response_util(
                status="error",
                message="No banners found.",
                data=[],
                http_status_code=404
            )

        return response_util(
            status="success",
            message="Banners fetched successfully.",
            data=active_banners,
            http_status_code=200
        )

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_all_banners failed")
        return response_util(
            status="error",
            message="An error occurred while fetching banners.",
            data=None,
            error=str(e),
            http_status_code=500
        )
