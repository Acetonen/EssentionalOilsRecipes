#!/usr/bin/env python3
"""Information about essential oils."""


class Oil:
    """Information about essential oils."""
    def __init__(self, name, volume):
        self.oil_name = name
        self.volume = volume

    def __str__(self):
        """Pretty print of Oil object"""
        return '{0} - {1} drops'.format(self.oil_name, self.volume)
