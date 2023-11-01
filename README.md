llamanator
==========

To run, use `python llamantor.py`. Needs OPENAI api-compatible key 
and host URL in the relevant environment variables. See `api.py` for
more info.

The knowledge store mechanism uses ./storage/ directory for storing the
stores, so that directory must exist for this feature to work properly.

This project heavily borrows concepts from [atisharma/llama_farm](https://github.com/atisharma/llama_farm)
