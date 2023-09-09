# ragman

Retrieval augmented generation for manual pages

# Todo

* Embeddings are simply every 512 tokens. Ideally CLS tokens should be generated for individual statements with the maximum available context.
* Actually load everything into a Milvus collection.
* Search functionality
* Permit using alternate models
* PyTorch (or alternative) interface for alternative models (for either preprocessing or embedding itself).

# Chunking

* Currently done via spaCy library using their small English model. Currently chunked by what the model considers a "sentence."
* Better results may be doable by using a span categorizer.
    * https://spacy.io/api/spancategorizer#ngram_suggester
    * Suggest all spans of at least length min_size and at most length max_size (both inclusive). Spans are returned as a ragged array of integers. The array has two columns, indicating the start and end position.
