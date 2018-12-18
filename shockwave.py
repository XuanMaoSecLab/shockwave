#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author = Tri0nes

from lib.parse import parse_args
from lib.manager import module_selector


def main():
    args = parse_args()
    module_selector(args)


if __name__ == "__main__":
    main()
