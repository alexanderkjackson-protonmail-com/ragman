import spacy
from spacy.tokens import Doc
import os
import pickle
import logging
from tools import preprocessors

logLevel = os.environ.get('PYTHON_LOGLEVEL', default='ERROR')
logging.basicConfig(level=logLevel)
# ./.pickle/./datasets/zshall.txt
cachePath = "./.pickle/"

""" TODO
1. Refactor variable names for consistent camelCase and good, meaningful names.
2. Refactor TextProcessor methods such that parameters default to self but are
    listed explicitly/may be outside the current object.
3. Reorder methods within TextProcessor class.
4. More error checking and class-based custom exceptions.
"""


class TextProcessor:
    def pickleLoad(self, picklePath):
        logging.debug("Loading from pickle: {}".format(picklePath))
        with open(picklePath, 'rb') as pickleFile:
            cachedTextProcessor = pickle.load(pickleFile)
            self.__dict__.update(cachedTextProcessor.__dict__)
            return

    def ingest(self, file):
        self.filePath = file
        logging.debug('Ingesting dataset {}'.format(file))
        with open(file, 'r', encoding='utf-8') as dataset:
            self.text = dataset.read()

    def pickleSave(self, file):
        """
        Saves current class instance to a pickle file.
        Overrides pickleFile attribute.
        """
        self.picklePath = file
        with open(file, 'wb') as pickleFile:
            pickle.dump(self, pickleFile)

    def docChunk(self, text=None, chunk_size=None):
        """
        Chunks into a stack of docs, respecting max 1,000,000 characters for
        doc.
        """
        # TODO: Check if text is empty and throw error if so.
        # Consider: Unsure if we want to use self.nlp here. Need to decide
        # whether to make parameters visible for these functions.
        if text is None:
            text = self.text
        if chunk_size is None:
            chunk_size = self.chunk_size
        for i in range(0, len(text), chunk_size):
            doc = self.nlp(text[i:i + chunk_size])
            self.docs_stack.append(doc)

    def __init__(self,
                 filePath,
                 chunk_size=1000000,
                 model='en_core_web_sm',
                 cache=True
                 ):
        """
        Initializes the TextProcessor with the given filePath and an optional
        line limit and spaCy model.

        :param filePath: The path to the text file to process.
        :param chunk_size: The maximum number of lines to read from the file.
        Defaults to None, which means all lines are read.
        :param model: The spaCy model to use for NLP tasks.
        Defaults to 'en_core_web_sm'.
        """
        # {{{ Boilerplate assignments for init.
        self.filePath = filePath
        self.chunk_size = chunk_size
        self.nlp = spacy.load(model)
        self.docs_stack = []
        self.sentences = []
        self.sentArray = []
        self._preprocess_funcs = []
        # }}}

        # Set picklePath based off stripped filePath
        self.picklePath = cachePath + self.filePath.lstrip('./')
        logging.debug("Cache file:{}".format(self.picklePath))

        os.makedirs(os.path.dirname(self.picklePath), exist_ok=True)

        # {{{ Load from Pickle file if caching enabled.
        # Rework this? Do not want to save pickleFile as an attribute.
        if cache is True and os.path.exists(self.picklePath):
            logging.debug('Reading cache file {}'.format(self.picklePath))
            self.pickleLoad(self.picklePath)
            return
        # }}}
        self.ingest(self.filePath)

        # Initial chunking to respect max initialization size for Doc object.
        if self.text is not None:
            self.docChunk(self.text, self.chunk_size)
            # Concantenate all the docs for convenience.
            self.c_doc = Doc.from_docs(self.docs_stack)
            del self.docs_stack  # Have to test this deletion is safe!

        # Save instance to picklePath.
        # TODO: Change to json. Add compression.
        if cache is True:
            logging.debug('Writing cache file {}'.format(self.picklePath))
            self.pickleSave(self.picklePath)

    def __getitem__(self, index):
        """
        Simply a test for subscript access.
        This needs to be placed into a special subscripting method.
        """
        # {{{ Convert entire doc to list of chunks
        if not self.sentArray:
            for sent in self.c_doc.sents:
                self.sentArray.append(sent.text)
        # }}}
        if isinstance(index, slice):
            return self.sentArray[index.start:index.stop:index.step]
        else:
            return self.sentArray[index]

    def get_sentence(self):
        """
        Yields sentences from the file up to the specified line limit using the
        spaCy sentence segmentation.
        """

        # for sentence in docs.sents:

        for sent in self.c_doc:
            yield sent
        """
        for i, line in enumerate(self.text):
            if self.chunk_size and i >= self.chunk_size:
                break
            doc = self.nlp(line)
            self.chunks.append((doc, line))
            print("i = {} line limit = {}".format(i, self.chunk_size))
            for sentence in doc.sents:
                yield sentence.text
        """
    # }}}

    def add_preprocess(self, func):
        """
        Adds a pre-processing function.
        """
        self._preprocess_funcs.append(func)

    def set_sentence_boundary_detection(self, boundary_detector):
        self.nlp.add_pipe(boundary_detector, before='parser')

    def custom_sentence_boundary_detector(self, doc):
        # Your custom sentence boundary detection logic here
        pass

    """
    # Not necessary if not storing the pickle file.
    def __reduce__(self):
        attributes = self.__dict__.copy()
        attributes.pop('file', None)
        return (self.__class__,
                (self.pickleFile,),
                attributes
                )
    """


"""
# Usage:

# Create an instance of the TextProcessor class
processor = TextProcessor('path/to/your/textfile.txt', chunk_size=10)

# Set a custom sentence boundary detector (optional)
# processor.set_sentence_boundary_detection(
    processor.custom_sentence_boundary_detector
    )

# Use the sentence_generator method to iterate over sentences
for sentence in processor.get_sentence():
    print(sentence)
"""
