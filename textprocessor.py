import spacy
from spacy.tokens import Doc
import os
import pickle
import logging

logLevel = os.environ.get('PYTHON_LOGLEVEL', default='ERROR')
logging.basicConfig(level=logLevel)
# ./.pickle/./datasets/zshall.txt
cachePath = "./.pickle/"


class TextProcessor:
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

        # Set picklePath based off stripped filePath
        self.picklePath = cachePath + filePath.lstrip('./')
        logging.debug("Cache file:{}".format(self.picklePath))

        os.makedirs(os.path.dirname(self.picklePath), exist_ok=True)

        # {{{ Load from Pickle file if caching enabled.
        # Rework this? Do not want to save pickleFile as an attribute.
        logging.debug("Test debug")
        if cache is True and os.path.exists(self.picklePath):
            logging.debug('Pickle file found. Loading from pickle.')
            with open(
                self.picklePath,
                # "./.pickle/{}".format(filePath),
                'rb'
            ) as pickleFile:
                cachedTextProcessor = pickle.load(pickleFile)
                self.__dict__.update(cachedTextProcessor.__dict__)
                return
        # }}}
        # {{{ Boilerplate assignments for init.
        self.filePath = filePath
        self.chunk_size = chunk_size
        self.nlp = spacy.load(model)
        self.docs_stack = []
        self.sentences = []
        self.sentArray = []
        self._preprocess_funcs
        # }}}
        with open(self.filePath, 'r', encoding='utf-8') as file:
            self.text = file.read()

        # {{{ Chunk text into stack of docs
        for i in range(0, len(self.text), chunk_size):
            doc = self.nlp(self.text[i:i + chunk_size])
            self.docs_stack.append(doc)
        # }}}

        self.c_doc = Doc.from_docs(self.docs_stack)
#         # {{{ Convert generators into list for subscriptable access
        for sent in self.c_doc.sents:
            self.sentArray.append(sent.text)
#         for doc in self.docs_stack:
#             for sent in doc.sents:
#                 self.sentences.extend(str(sent))
#             # self.sentences.extend(list(doc.sents))
#         # }}}

        # {{{ Cache new object via pickle
        # if cache is True and os.path.exists(self.picklePath):
        if cache is True:
            logging.debug('Writing cache file {}'.format(self.picklePath))
            with open(
                self.picklePath,
                'wb'
            ) as pickleFile:
                pickle.dump(self, pickleFile)
        # }}}

    def __getitem__(self, index):
        """
        Simply a test for subscript access.
        This needs to be placed into a special subscripting method.
        """
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
#        for doc in self.docs_stack:
#            for sent in doc.sents:
#                yield sent
        # with open(self.filePath, 'r', encoding='utf-8') as file:
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
