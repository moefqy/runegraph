# RuneGraph: Blog Cover Generator

## Introduction

A lightweight Python tool that generates stylized blog cover images from a title, subtitle, and configurable style options. Built on [Pillow](https://pillow.readthedocs.io/en/stable/).

## Features

- Multi-line title support with automatic horizontal centering
- Optional logo overlay (top-left, configurable size and margin)
- Configurable font paths, colors, font sizes, and output format (PNG, JPG, WEBP)
- Validated config via `set_cover_config()` — rejects invalid colors, sizes, and formats early
- Output saved to a configurable directory with auto-slugified filenames

## How to use?

### Directory Structure

```
runegraph/
├── assets/
│   ├── fonts/          # Custom .ttf font files
│   └── img/            # Logo or other image assets
├── notebooks/
│   └── main.ipynb      # Interactive usage notebook
├── src/
│   ├── generator.py    # Core image generation logic
│   └── utils.py        # Config dataclass and validation helpers
└── requirements.txt
```

### Getting Started

To get started, follow these steps:

1. Clone the Repository:
   
   ```bash
   git clone https://github.com/moefqy/runegraph.git
   cd runegraph
   ```

2. Set Up the Python Environment:
   
   Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

    Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Notebook:

   Open `notebooks/main.ipynb` in Jupyter and run all the cells.

   > **Note:** `set_cover_config()` to configure style options and `generate_blog_cover()` to produce the image.

4. Or, generate the cover directly using the Python script below.

    ```python
    from src.utils import set_cover_config
    from src.generator import generate_blog_cover

    config = set_cover_config(
        background_color="#0f172a",
        text_color="#dedadc",
        font_size_title=45,
        font_size_subtitle=15,
        output_format="PNG",
        output_dir="./output",
    )

    output_path = generate_blog_cover(
        title="My Blog Post",
        subtitle="Written by Heisenberg",
        config=config,
        title_font_path="assets/fonts/raleway-thin.ttf",
        subtitle_font_path="assets/fonts/raleway.ttf",
        logo_path="assets/img/logo.png",
    )

    print(f"Cover saved to: {output_path}")
    ```

## Configuration Reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | `int` | `1000` | Canvas width in pixels |
| `height` | `int` | `420` | Canvas height in pixels |
| `background_color` | `str` | `"#0f172a"` | Hex color for the background |
| `text_color` | `str` | `"#dedadc"` | Hex color for title and subtitle text |
| `font_size_title` | `int` | `45` | Title font size |
| `font_size_subtitle` | `int` | `15` | Subtitle font size |
| `vertical_margin` | `int` | `15` | Extra gap (px) between title block and subtitle |
| `line_gap` | `int` | `15` | Gap (px) between title lines |
| `output_format` | `str` | `"PNG"` | Output format: `PNG`, `JPG`, `JPEG`, or `WEBP` |
| `output_dir` | `str` | `"./output"` | Directory where images are saved |
| `logo_size` | `int` | `30` | Max logo dimension in pixels |
| `logo_margin` | `int` | `15` | Logo offset from the top-left corner |

## Preview

[![preview](notebooks/output/how_to_build_a_blog_cover_generator_using_pillow_in_python.png)](https://github.com/moefqy/runegraph)

## Contact

For any inquiries or feedback, you can reach me at moefqy@rocketmail.com.