import stripe

from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from config import settings
from .paginators import CoursesPaginator
from .permissions import IsManagers
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, Lesson, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer, CardInformationSerializer
from .servises import stripe_card_payment, save_payment_if_valid
from .validators import product_owner_validation


class CourseViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsManagers]
    permission_classes = [AllowAny]
    serializer_class = CourseSerializer
    pagination_class = CoursesPaginator

    def get_queryset(self):
        queryset = Course.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Создать новый урок.
    """
    #permission_classes = [IsManagers]
    permission_classes = [AllowAny]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonListAPIView(generics.ListAPIView):
    """
    Получить список всех уроков.
    """
    serializer_class = LessonSerializer
    pagination_class = CoursesPaginator

    def get_queryset(self):
        queryset = Lesson.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Получить конкретный урок.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Обновить существующий урок.
    """
    permission_classes = [AllowAny]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удалить существующий урок.
    """
    permission_classes = [IsManagers]
    queryset = Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """
    Получить список всех платежей.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('pay_course', 'payment_method')
    ordering_fields = ('pay_date',)
    pagination_class = CoursesPaginator


class PaymentAPIView(APIView):
    """
    Создать оплату
    """
    serializer_class = CardInformationSerializer

    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        payment = {
            'user': request.user,
            'pay_course': course
        }

        product_owner_validation(payment)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            stripe.api_key = settings.STRIPE_SECRET_KEY
            data_dict = serializer.data

            course_price = course.price
            response = stripe_card_payment(
                data_dict=data_dict,
                product_price=course_price
            )

            save_payment_if_valid(response, payment)

        else:
            response = {
                'errors': serializer.errors,
                'status': status.HTTP_400_BAD_REQUEST
            }

        return Response(response)
