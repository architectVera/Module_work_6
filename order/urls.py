""" URLS for the order app  """

from django.urls import path

from order.views import purchase_session, PurchaseSessionDetailView, PurchaseSessionListView

urlpatterns = [
    path('purchase/<int:pk>/', purchase_session, name='purchase-session'),
    path('purchase/<int:user_id>', PurchaseSessionListView.as_view(), name='purchase-list'),
    path('purchase/<int:user_id>/<int:purchase_id>', PurchaseSessionDetailView.as_view(), name='purchase_detail'),
    # path('purchase/<int:user_id>/<int:purchase_id>/refund/', RefundCreateView.as_view(), name='refund_create'),
    # path('refund/<int:user_id>', RefundProductListView.as_view(), name='refund_list'),
    # path('refund/<int:user_id>/<int:refund_id>', RefundProductDetailView.as_view(), name='refund_detail'),
    # path('refund/<int:user_id>/<int:refund_id>/delete',  RefundRejectDelView.as_view(), name='refund_reject'),
    # path('refund/<int:user_id>/<int:refund_id>/approve', refund_approve_product, name='refund_approve'),
]
