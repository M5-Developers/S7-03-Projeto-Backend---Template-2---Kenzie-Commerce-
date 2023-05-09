from rest_framework import generics
from .serializers import OrderSerializer
from .models import Order, ProductOrder
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.sendEmail import send_html
from accounts.models import Account
from accounts.permissions import IsSeller

class OrderView(generics.ListCreateAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	queryset = Order.objects.all()
	serializer_class = OrderSerializer

	def perform_create(self, serializer):
		send_html(self.request.user.email,'Pending')
		user = self.request.user
		serializer.save(user=user)

		order_id = serializer.data['id']
		products = user.cart.products.get_queryset()
		
		for product in products:
			ProductOrder.objects.create(order_id=order_id, product=product, quantity=user.cart.cart_products.select_related().get(product_id=product.id).quantity)


class OrderViewDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSeller]

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        order_pk=self.kwargs['pk']
        order_obj= Order.objects.get(id=order_pk)
        user_email=Account.objects.get(id=order_obj.user_id).email
        send_html(user_email,self.request.data['status'])
        
        serializer.save()
		
class OrderInAccountView(generics.ListAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	queryset = Order.objects.all()
	serializer_class = OrderSerializer

	def get_queryset(self):
		orders = self.queryset.filter(user_id=self.request.user.id)
		
		return orders
