# Super-Dolphin

Super-Dolphin is an advanced remake of the original Dolphin project. This new version now features a PyQt5 designer to define the layout of videos with text fields that can be processed in batches using a CSV file. This project is currently under heavy development and is maintained by Cognispark for educational purposes to promote tutoring services.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Designing Layouts](#designing-layouts)
  - [Creating Videos in Batch](#creating-videos-in-batch)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install Super-Dolphin, follow these steps:

```sh
cd ~
git clone https://www.github.com/Ubuntufanboy/Super-Dolphin.git
```

## Usage

### Designing Layouts

You can design the video layouts using the PyQt5 designer. To launch the designer, run:

```sh
python3 ~/Super-Dolphin/design/main.py
```

This will open the PyQt5 interface where you can create and customize your video layouts. Once you're satisfied with your design, export the layout information to `layouts.json`.

### Creating Videos in Batch

With your layout defined in `layouts.json`, you can create videos in batches by running:

```sh
python3 ~/Super-Dolphin/src/main.py
```

This script processes the layouts and a provided CSV file to generate videos using `ffmpeg-python`.

## Contributing

All contributions are welcome! If you wish to contribute, please note the following:

- Ensure your pull request clearly states the purpose of the code change.
- All code changes will undergo peer review by one of our employees.
- Code contributions may not be merged if they do not meet the required standards.

## License

This project is maintained for educational purposes by Cognispark and is intended to promote tutoring services. The project does not currently exist on PyPI.
