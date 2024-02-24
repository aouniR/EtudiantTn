from django.urls import path
from .views import test_offers,take_test,begin_test,delete_session_key

urlpatterns = [
    path('', test_offers, name='test_offers'),
    path('begin_test/<int:test_id>/<int:question_id>', begin_test, name='begin_test'),
    path('take_test/<int:test_id>', take_test, name='take_test'),
    path('delete_session_key/', delete_session_key, name='delete_session_key'),
]