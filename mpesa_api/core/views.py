from celery import chain
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from mpesa_api.core.tasks import process_b2c_result_response_task, \
    process_c2b_confirmation_task, process_c2b_validation_task, \
    handle_online_checkout_callback_task


class B2cTimeOut(APIView):
    """
    Handle b2c time out
    """
    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        return Response(dict(success="0"))


class B2cResult(APIView):
    """
    Handle b2c result
    """
    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        chain(process_b2c_result_response_task.s(data)).apply_async(queue='b2c_result')
        return Response(dict(success="0"))


class C2bValidation(APIView):
    """
    Handle c2b Validation
    """
    @csrf_exempt
    def post(self, request, format=None):
        """
        process the c2b Validation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        chain(process_c2b_validation_task.s(data)).apply_async(queue='c2b_validation')
        return Response(dict(accept="0"))


class C2bConfirmation(APIView):
    """
    Handle c2b Confirmation
    """
    @csrf_exempt
    def post(self, request, format=None):
        """
        process the confirmation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        chain(process_c2b_confirmation_task.s(data)).apply_async(queue='c2b_confirmation')
        return Response(dict(accept="0"))


class OnlineCheckoutCallback(APIView):
    """
    Handle online checkout callback
    """
    @csrf_exempt
    def post(self, request, format=None):
        """
        process the confirmation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        chain(handle_online_checkout_callback_task.s(data)).apply_async(queue='online_checkout_callback')
        return Response(dict(accept="0"))