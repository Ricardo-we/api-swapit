from django.urls import path
from api.views.users import create_user, login, get_users, confirm_user_creation, users_detail
from api.views.products import add_product, get_products, product_details, delete_product_as_superuser
from api.views.user_contact_info import add_user_contact_info, contact_info_details
from api.views.product_images import add_product_image, delete_product_image
from api.views.tags import add_tag, tags_detail, get_tags
from api.views.reports import report_product

ENDPOINTS = [
    'users',
    'products',
    'tags'
]

urlpatterns = [
    path(f'{ENDPOINTS[0]}/sign-up', create_user),
    path(f'{ENDPOINTS[0]}/sign-up/confirm/<str:confirmation_code>',
         confirm_user_creation),
    path(f'{ENDPOINTS[0]}/login', login),
    path(f'{ENDPOINTS[0]}', get_users),
    path(f'{ENDPOINTS[0]}/<int:pk>', users_detail),

    # USER CONTACT-INFO PATHS
    path(f'{ENDPOINTS[0]}/contact-info/<int:user_id>', add_user_contact_info),
    path(f'{ENDPOINTS[0]}/contact-info/<int:user_id>/<int:contact_id>',
         contact_info_details),

    # PRODUCT PATHS
    path(f'{ENDPOINTS[1]}', get_products),
    path(f'{ENDPOINTS[1]}/<int:user_id>/add', add_product),
    path(f'{ENDPOINTS[1]}/<int:user_id>/<int:pk>', product_details),
    # PRODUCT_IMAGES_PATH
    path(f'{ENDPOINTS[1]}/images/<int:user_id>/add', add_product_image),
    path(f'{ENDPOINTS[1]}/images/<int:user_id>/<int:image_id>',
         delete_product_image),
    # REPORTS
    path(
        f'{ENDPOINTS[1]}/report/<int:user_id>/<int:product_id>', report_product),
    # DELETE PRODUCT AS SUPERUSER
    path(f'{ENDPOINTS[1]}/<int:user_id>/<int:product_id>/as-superuser',
         delete_product_as_superuser),
    # path(f'{ENDPOINTS[1]}', get_users),

    # TAGS (ONLY ADMINS)
    path(f'{ENDPOINTS[2]}', get_tags),
    path(f'{ENDPOINTS[2]}/<int:user_id>', add_tag),
    path(f'{ENDPOINTS[2]}/<int:user_id>/<int:tag_id>', tags_detail),
]
