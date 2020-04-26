# Playsation 3 Update Downloader

This is a simple script to download updates for a specific PS3 title.

## Requirements

The latest Python 3. I made sure that this does not require installing external libraries or setting up a VM.

## Arguments

The script takes a number of titleid as positional arguments and a number of optional arguments.
 * -e, --env: Changes the "environment" part of the url. Defaults to np
 * -o, --output: Changes the output folder to download updates to
 * -q, --quiet: Remove all output messages

## TODO List

There are a number of things I would like to do to improve on this
 * Linting: I could use black as a linter to clean up the code.
 * Fix certificate validation when downloading pkg files. Right now, the certificate served does not have the right domain name and it fails validation
 * Graphical interface: Make it easier to run this program by giving it a GUI
 * Integration with RPCS3 / other emulators: It could be interesting to integrate this with emulators to simplify downloading of updates files.
 * Modularize: Make it so that this can be run from the command-line or through another program as a module. This could simplify adding a GUI or intergrating with existing emulators.
