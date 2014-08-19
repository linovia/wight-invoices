
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'invoice', views.Invoice, base_name='api-invoice')
urlpatterns = router.urls
