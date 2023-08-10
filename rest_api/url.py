from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
    path('product/<int:product_id>/',ProductReview.as_view(),name='product-View'),
    path('order/<int:order_id>/',AllOrderItems.as_view(),name='Oreder_view'),
    path('search/',SearchProductView.as_view(),name='search-product'),
    path('search/filter/',ProductFilterView.as_view(),name='search-product'),
    path('Allproduct/',ProductPaginatorView.as_view(),name='All-product'),
    path('search/allfeature/',ProductSearchPaginatorView.as_view(),name='All-product'),
    path('search/pricerange/',ProductViewPriceRange.as_view(),name='Product-View-Price-Range'),
    path('search/multifilter/',ProductMultifillter.as_view(),name='filter-mulit-product'),
    path('search/namedesc/',ProductSearchNameDesc.as_view(),name='search-name-desc-product'),
    path('user/signup/',csrf_exempt(SignUpView.as_view()),name='user-signup'),
    path('user/signin/',csrf_exempt(SignInView.as_view()),name='user-signin'),
    path('productAll/',ProductView.as_view(),name='All-product'),

]