#!/usr/bin/env python3
import click


@click.command()
@click.option("--exec",
              type=click.Path(dir_okay=False, file_okay=True, exists=True),
              help="Path to the CK III game")
@click.option("-n", default=10, help="Number of output pictures")
@click.option("--folder", type=click.Path(dir_okay=True, file_okay=False),
                default="faces",
                help="Output folder for generated faces")
def hello(exec, n, folder):
    print(exec, n, folder)

if __name__=="__main__":
    hello()