# -*- coding: utf-8 -*-

"""Console script for vibrant_frequencies."""
import logging

import click
from .prototype import visualize


@click.command()
def main():
    logging.getLogger('').setLevel(logging.WARN)
    visualize()


if __name__ == "__main__":
    main()
