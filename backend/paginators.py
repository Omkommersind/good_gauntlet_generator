from base64 import b64encode
from collections import OrderedDict
from urllib import parse

from rest_framework.pagination import LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class LimitOffsetPaginationDataAndCountOnly(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('results', data)
        ]))


class CustomCursorPagination(CursorPagination):
    ordering = '-timestamp'
    page_size = 20

    def encode_cursor(self, cursor):
        """
        Given a Cursor instance, return an url with encoded cursor.
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = parse.urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return encoded
