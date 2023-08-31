# ragman
Retrieval augmented generation for manual pages

# Todo:
* Embeddings are simply every 512 tokens. Ideally CLS tokens should be generated for individual statements with the maximum available context.
* Actually load everything into a Milvus collection.
* Search functionality
* Permit using alternate models
* PyTorch (or alternative) interface for alternative models (for either preprocessing or embedding itself).
