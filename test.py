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

    print('Running test of textprocessor')
    txt = TextProcessor(
        filePath=args.file if args.file is not None else
        "./datasets/zshall.txt",
        chunk_size=args.number if args.number is not None else
        1000000,
        model=args.model if args.model is not None else
        "en_core_web_sm"
    )
    sentences = txt.get_sentence()
    """
    iterator = 0
    for sentence in txt.get_sentence():
        iterator += 1
        # print("Statement {}: {}".format(iterator, sentence))
        print("Chunks: {}".format(sentence))
    """
