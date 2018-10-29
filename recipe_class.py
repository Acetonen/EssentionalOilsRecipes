#!/usr/bin/env python3
"""Class contain name of recipe, containing oils, recipe raiting."""


class Recipe:
    """Class contain name of recipe, containing oils, recipe raiting."""
    def __init__(self, name, oil, rating):
        self.name = name
        self.oils = oil
        self.rating = rating

    def __str__(self):
        """Beauty output of classs objects"""
        oils_print = ''
        for oil in self.oils:
            string = "{} - {}drop".format(
                self.oils[oil].oil_name, str(self.oils[oil].volume))
            oils_print = oils_print + string + '; '
        return ('{0} \n\trating: ({1}/10) \n\tcomposition: {2}'.format(
            self.name, self.rating, oils_print))
