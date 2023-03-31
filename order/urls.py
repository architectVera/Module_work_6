""" URLS for the order app  """

from django.urls import path

from order.views import purchase_session, PurchaseSessionDetailView, PurchaseSessionListView

urlpatterns = [
    path('purchase/<int:pk>/', purchase_session, name='purchase-session'),
    path('purchase/<int:user_id>', PurchaseSessionListView.as_view(), name='purchase-list'),
    path('purchase/<int:user_id>/<int:purchase_id>', PurchaseSessionDetailView.as_view(), name='purchase_detail'),
]
