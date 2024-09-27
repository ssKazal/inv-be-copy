import math
from typing import Union
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"

    def _get_next_page(self) -> Union[int, None]:
        if not self.page.has_next():
            return None
        page_number: int = self.page.next_page_number()
        return page_number

    def _get_previous_page(self) -> Union[int, None]:
        if not self.page.has_previous():
            return None
        page_number: int = self.page.previous_page_number()
        return page_number

    def _get_total_page(self) -> Union[int, None]:
        count = self.page.paginator.count
        page_size = self.get_page_size(self.request)

        return math.ceil(count / page_size)

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page_size": self.get_page_size(self.request),
                "next": self._get_next_page(),
                "previous": self._get_previous_page(),
                "total_page": self._get_total_page(),
                "results": data,
            }
        )

class CustomOneTimeGoodsPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"

    def _get_next_page(self) -> Union[int, None]:
        if not self.page.has_next():
            return None
        page_number: int = self.page.next_page_number()
        return page_number

    def _get_previous_page(self) -> Union[int, None]:
        if not self.page.has_previous():
            return None
        page_number: int = self.page.previous_page_number()
        return page_number

    def _get_total_page(self) -> Union[int, None]:
        count = self.page.paginator.count
        page_size = self.get_page_size(self.request)

        return math.ceil(count / page_size)

    def get_paginated_response(self, data):
        return Response(
            {
                "onetime_goods_count": self.page.paginator.count,
                "onetime_goods_page_size": self.get_page_size(self.request),
                "onetime_goods_next": self._get_next_page(),
                "onetime_goods_previous": self._get_previous_page(),
                "onetime_goods_total_page": self._get_total_page(),
                "onetime_goods_results": data,
            }
        )

class CustomOldOneTimeGoodsPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"

    def _get_next_page(self) -> Union[int, None]:
        if not self.page.has_next():
            return None
        page_number: int = self.page.next_page_number()
        return page_number

    def _get_previous_page(self) -> Union[int, None]:
        if not self.page.has_previous():
            return None
        page_number: int = self.page.previous_page_number()
        return page_number

    def _get_total_page(self) -> Union[int, None]:
        count = self.page.paginator.count
        page_size = self.get_page_size(self.request)

        return math.ceil(count / page_size)

    def get_paginated_response(self, data):
        return Response(
            {
                "old_onetime_goods_count": self.page.paginator.count,
                "old_onetime_goods_page_size": self.get_page_size(self.request),
                "old_onetime_goods_next": self._get_next_page(),
                "old_onetime_goods_previous": self._get_previous_page(),
                "old_onetime_goods_total_page": self._get_total_page(),
                "old_onetime_goods_results": data,
            }
        )

import logging
class BazarGoodsPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"

    def _get_next_page(self) -> Union[int, None]:
        logging.debug("Getting next page")
        if not self.page.has_next():
            return None
        page_number: int = self.page.next_page_number()
        return page_number

    def _get_previous_page(self) -> Union[int, None]:
        logging.debug("Getting previous page")
        if not self.page.has_previous():
            return None
        page_number: int = self.page.previous_page_number()
        return page_number

    def _get_total_page(self) -> Union[int, None]:
        count = self.page.paginator.count
        page_size = self.get_page_size(self.request)

        return math.ceil(count / page_size)

    def get_paginated_response(self, data):
        return Response(
            {
                "bazar_count": self.page.paginator.count,
                "bazar_page_size": self.get_page_size(self.request),
                "bazar_next": self._get_next_page(),
                "bazar_previous": self._get_previous_page(),
                "bazar_total_page": self._get_total_page(),
                "bazar_results": data,
            }
        )
