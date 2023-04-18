# Extractive-QA-Annotation
This is a package for cleaning and preparing a corpus of text-scraped web pages as input for a downstream Question-Answer annotation task.

## Features

* Converting markdown files into plain text
* Removing headers, images, links from the document
* A simple filtering mechanism so that only documents relevant to a particular topic are maintained.

## Installation

To install the necessary dependencies, run:

```
pip install -r requirements.txt
```

## Usage

First, prepare a corpus of documents as plain text or Markdown files and place them in a suitable directory.

To use the package, follow these steps:

1. Define a list of keywords that represent a topic of interest. This package has been designed to extract documents related to Asthma, so a short list of keywords is included as default.


2. Run the data cleaning and preparation step from the command line by running ```python main.py /path/to/input/documents /path/to/output/directory --keywords keyword1 keyword2 keyword3```. You will see A ```Documents processed``` message in your terminal when the script has completed. Alternatively, documents can be cleaned within python by running ```run_process_docs.py``` within VS Code. In future, I may also add a notebook version.


## Contributing

If you have any suggestions, improvements, or bug reports, please feel free to submit an issue or create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.