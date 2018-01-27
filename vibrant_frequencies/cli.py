# -*- coding: utf-8 -*-

"""Console script for vibrant_frequencies."""
import logging

import click
from .prototype import Prototype


@click.command()
def main(args=None):
    logging.getLogger('').setLevel(logging.WARN)
    """Console script for vibrant_frequencies."""
    Prototype()


if __name__ == "__main__":
    main()
