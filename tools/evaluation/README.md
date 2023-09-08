# Evaluation tools

Here is a collection of evaluation tools which will be useful for assessing the
quality of embeddings.

Massive Text Embedding Benchmark: <https://github.com/embeddings-benchmark/mteb>

# STS (Semantic Similarity) benchmark - Useful for evaluating embeddings for  
sentences for doc retrieval?

Semantic Similarity: <https://github.com/muralikrishnasn/semantic_similarity>

An issue with these is that they are not intended necessarily for evaluating
quality for document retrieval. It will be useful to retrieve information
that's similar to the prompt itself, but the prompt will be interrogative
whereas the documentation will not be. There are a couple potential solutions for this:
*Pre-processing into question/answer pairs using a fairly large, general-purpose GPT.
*Pre-processing queries into statements, guessing at retrieved information.
*Must be other good methods.
