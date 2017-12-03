# -*- coding: utf-8 -*-

"""Console script for vibrant_frequencies."""

import click
from vibrant_frequencies.prototype import visualize


@click.command()
def main(args=None):
    """Console script for vibrant_frequencies."""
    visualize()


if __name__ == "__main__":
    main()
