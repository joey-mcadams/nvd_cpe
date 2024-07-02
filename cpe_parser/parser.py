from __future__ import annotations

import urllib
from typing import Dict, List

from cpe_parser.errors import CpeFormatError


class CpeParser:
    def __init__(self) -> None:
        self.format_prefix: str = "cpe:2.3:"
        self.uri_prefix: str = "cpe:/"
        self.uri_binding_delimiterKey: str = ':~'
        self.cpe_attributes: List[str] = ["part",
                                           "vendor",
                                           "product",
                                           "version",
                                           "update",
                                           "edition",
                                           "language",
                                           "sw_edition",
                                           "target_sw",
                                           "target_hw",
                                           "other"]

    def parser(self, cpe: str) -> Dict[str, any]:
        """
        Parses given cpe value both in uri or formatted.

        return: An attribute value dictionary
        """
        full_cpe: str = cpe.strip().lower()
        full_cpe_decoded: str = urllib.parse.unquote(full_cpe)

        if not (self.__validateUri(full_cpe_decoded) or self.__validateFS(full_cpe_decoded)):
            raise CpeFormatError(f"given cpe {full_cpe_decoded} does not match cpe formats")

        substring: str = self.__sub_string(full_cpe_decoded)
        attributes: List[str] = self.__get_attributes(full_cpe_decoded, substring)
        cpe_values: dict[str, any] = dict(zip(self.cpe_attributes, attributes))

        # Normalization
        # TODO: There's a better way to do this
        cpe_values['vendor'] = cpe_values['vendor'].replace("\\", "")
        cpe_values['name'] = cpe

        return cpe_values

    def __get_attributes(self, cpe: str, cpe_attributes: str) -> List[str]:
        """
        Returns attributes of the cpe
        """
        attributes: list[str] = cpe_attributes.split(":")
        if self.__is_uri_binding_cpe(cpe) or self.uri_binding_delimiterKey not in cpe:
            return attributes

    def __sub_string(self, cpe: str) -> str:
        """
        Retrive the substring of the cpe
        """
        if self.__is_formated_binding_cpe(cpe):
            return cpe[len(self.format_prefix):]

        return cpe[len(self.uri_prefix):]

    def __validateUri(self, value: str) -> bool:
        """
        Validate given uri biding cpe
        """
        if not value.startswith(self.uri_prefix):
            return False
        return True

    def __validateFS(self, value: str) -> bool:
        """
        Validate given formatted cpe
        """
        if not value.startswith(self.format_prefix):
            return False
        return True

    def __is_formated_binding_cpe(self, cpe: str) -> bool:
        """
        Check if the cpe is formatted or not
        """
        return cpe.startswith(self.format_prefix)

    def __is_uri_binding_cpe(self, cpe: str) -> bool:
        """
        Check if the cpe is uri binding or not
        """
        return cpe.startswith(self.uri_prefix)
