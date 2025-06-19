# Compact Packing of Gates

A Python-based solution for efficiently packing gates of various dimensions onto a chip using a bin packing optimization algorithm.

## Project Overview

This project implements a compact packing algorithm for VLSI (Very Large Scale Integration) gate placement. The goal is to place gates of different dimensions on a chip in a way that minimizes the total area used. This is a critical step in chip design as it directly impacts the final size and cost of integrated circuits.

## Features

- Reads gate dimensions from an input file
- Implements an optimized bin packing algorithm
- Prioritizes gates based on size for better packing
- Generates coordinates for each gate placement
- Visualizes the final gate placement using a graphical interface
- Calculates the total area utilization

## Data Structures Used

1. **Dictionaries**: Used for storing gate dimensions and placement coordinates
2. **Lists**: Used for managing empty spaces during the packing process
3. **Tuples**: Represent dimensions and coordinates of gates and spaces

## Algorithm Flow

1. **Input Processing**:
   - Gates are read from the input file with their dimensions (width and height)
   - Each gate is stored in a dictionary with its name as key and dimensions as value
   - This dictionary provides quick access to gate dimensions throughout the packing process

2. **Gate Sorting**:
   - Gates are sorted in descending order based on their maximum dimension (either width or height)
   - This sorting is crucial for optimization - placing larger gates first tends to result in more efficient space usage
   - The sorting uses a key function: `max(width, height)` to prioritize gates with largest dimensions

3. **Space Management**: 
   - The algorithm maintains a list `L` of empty rectangular spaces sorted by area (largest first)
   - Each space is represented as a tuple: `(width, height, x, y)` where (x,y) are coordinates
   - Initially, there's one space with the dimensions of the first (largest) gate at position (0,0)
   - As gates are placed, spaces are dynamically split, removed and added to this list

4. **Placement Strategy**:
   - For each gate, the algorithm performs:
     - **Best-Fit Search**: Finds the smallest suitable space that can accommodate the gate using `find_fitting_node()`
     - **Space Utilization**: If a suitable space is found, places the gate at the bottom-left corner of that space
     - **Space Splitting**: After placement, the remaining area is split into two new rectangular spaces using `make_two_new_empty_spaces()`
     - **Heuristic Split**: The split direction (horizontal vs vertical) is chosen to maximize the usefulness of the remaining spaces
     - **Space Sorting**: New spaces are inserted into the list maintaining the descending area order

5. **Bounding Box Expansion**:
   - If no existing space fits the gate, the bounding box is expanded using `add_new_block()`
   - The algorithm decides whether to expand vertically or horizontally based on a heuristic:
     - If extending upward would waste less space than extending right, it chooses upward expansion
     - Otherwise, it extends to the right
   - After expansion, a new space is created in the newly allocated area
   - The bounding box coordinates are updated to reflect the new chip dimensions

6. **Coordinate Assignment**:
   - For each gate placement, coordinates are stored in the `gates` dictionary
   - Coordinates represent the bottom-left corner (x,y) position of each gate
   - The coordinate system has (0,0) at the bottom-left corner of the chip

7. **Output Generation**: 
   - The final bounding box dimensions (chip size) are written to the output file
   - Gate placements with their coordinates are written in the format: `[gate_name] [x] [y]`
   - Gates are output in alphanumeric order for readability
   - A utilization metric is calculated to assess packing efficiency

## Requirements

- Python 3.x
- Tkinter (for visualization)
- PIL (Python Imaging Library / Pillow)

## Installation

```bash
# Install required packages
pip install tk
pip install pillow
```

## How to Run

1. Prepare an input file named `input.txt` with gate information in the format:
   ```
   [gate_name] [width] [height]
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

3. For visualization:
   ```bash
   python visualize_gates.py
   ```

## File Structure

- `main.py`: Core algorithm for gate packing
- `visualize_gates.py`: Visualization tool for the final placement
- `input.txt`: Input file containing gate dimensions
- `output.txt`: Generated output file with gate placements

## Algorithm Details

The algorithm uses a modified Best-Fit Decreasing (BFD) bin packing approach with these key strategies:

1. **Space Selection**: When placing a gate, the algorithm searches for the smallest available space that can fit the gate
2. **Space Splitting**: After placing a gate, the remaining space is split into two new rectangles
3. **Space Management**: Empty spaces are maintained in a sorted list for efficient searching
4. **Bounding Box Expansion**: When no suitable space is found, the bounding box is expanded either horizontally or vertically, whichever is more efficient

## Performance

The algorithm aims to maximize space utilization while maintaining a reasonable runtime complexity. The space utilization can be calculated as:
```
Utilization = (Sum of all gate areas) / (Final bounding box area)
```

## Future Improvements

- Implementation of alternative packing algorithms for comparison
- Support for rotated gates to further optimize placement
- Parallelization of the algorithm for handling large-scale designs
- Enhanced visualization with interactive features

## Acknowledgements

This project was developed as part of the COL215 course at IIT Delhi, focusing on data structures and algorithms for electronic design automation.
