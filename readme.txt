# Optus Topology Creator

## Description

This Python script processes CDP output files to generate network topology diagrams, orphan device reports, and `.graphml` files. It also post-processes the `.graphml` file to add yEd-compatible node labels for visualization in yEd.

## Features

- Parses CDP output files to build a network graph
- Identifies orphan devices and exports a CSV report
- Generates a topology diagram image
- Exports a standard `.graphml` file
- Adds yEd label markup to the `.graphml` file for proper display in yEd

## Requirements

- Python 3.x
- `networkx`
- `matplotlib`

Install dependencies:
## Usage

1. Place CDP output files in the input directory:
   `C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Input`

2. Run the script:

3. Find output files in:
   `C:\Users\JuanNava\PycharmProjects\PythonProject\Optus_Topology_Creator\Output`
   - Topology diagram: `<timestamp>.png`
   - Orphan report: `<timestamp>_orphans.csv`
   - yEd-compatible GraphML: `<timestamp>.graphml`

## Notes

- The script automatically adds yEd label markup to the GraphML file.
- Open the `.graphml` file in yEd for visualization.

## Project Structure

- `Graphene.py` — Main script
- `Helpers/` — Helper modules

## License

For internal and educational use.