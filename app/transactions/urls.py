
from django.urls import path
from transactions import views

urlpatterns = [
     path('create', views.CreateTransactionAPIView.as_view(),
          name="create-transaction"),
     path('validate/<slug:reference>/', views.ValidatePaymentAPIView.as_view(),
          name="validate-transaction"),
     path('<slug:reference>/', views.TransactionRetrieveDetail.as_view(),
          name="retrieve-transaction"),
     path('', views.ListCustomerTransactionAPIView.as_view(),
          name="customer-transaction"),
     path('list', views.ListTransactionAPIView.as_view(),
          name="list-customer-transaction"),
]
