from textprocessor import TextProcessor
from argparse import ArgumentParser
import os
import logging

logLevel = os.environ.get('PYTHON_LOGLEVEL', 'DEBUG')
logging.basicConfig(level=logLevel)

if __name__ == '__main__':
    # {{{ Setup arguments
    parser = ArgumentParser(description="Test description")
    parser.add_argument("-f",
                        "--file",
                        type=str,
                        required=False,
                        help="Path to input file to chunk"
                        )
    parser.add_argument("-n",
                        "--number",
                        type=int,
                        required=False,
                        help="Number of chunks to extract."
                        )
    parser.add_argument("-m",
                        "--model",
                        type=str,
                        required=False,
                        help="Chunking model to use. Default: en_core_web_sm"
                        )
    args = parser.parse_args()
    # }}}
"""
    print('Running test of textprocessor')
    txt = TextProcessor(
        filePath=args.file if args.file is not None else
        "./datasets/zshall.txt",
        chunk_size=args.number if args.number is not None else
        1000000,
        model=args.model if args.model is not None else
        "en_core_web_sm",
        cache=False
    )
    sentences = txt.get_sentence()
"""
# Testing use of TextProcessor without complete initialization.
txt = TextProcessor(filePath=None,
                    chunk_size=1000000,
                    model='en_core_web_sm',
                    )
txt.ingest('./datasets/short_example.txt')
print('Done')
