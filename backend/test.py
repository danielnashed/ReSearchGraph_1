from unstructured.partition.auto import partition
from unstructured.chunking.basic import chunk_elements
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import replace_unicode_quotes
from unstructured.cleaners.core import clean
from unstructured.cleaners.core import clean_non_ascii_chars
from unstructured.staging.base import convert_to_dict
import time


start=time.time()

# [1] Partition the PDF
elements = partition(url="https://arxiv.org/pdf/2502.08644",
                     infer_table_structure=False,
                     strategy="fast",
                     )

# [2] Chunk the elements
chunks_as_elems = chunk_by_title(elements,
                        max_characters=2000,
                        overlap=20)

# [3] Convert list of chunks (type = element) to list of dictionaries
chunks_as_dicts = convert_to_dict(chunks_as_elems)

# [4] Clean the chunks
chunks = []
for chunk in chunks_as_dicts:
    text = clean(chunk["text"], extra_whitespace=True, trailing_punctuation=True)
    text = clean_non_ascii_chars(text)
    text = replace_unicode_quotes(text)
    chunks.append(text)

end=time.time()
# print("\n\n************************\n\n".join([str(el) for el in chunks[:10]]))
print("\n\n************************\n\n".join([el for el in chunks[:10]]))
print("time taken",(end-start))
# print(len(chunks) * 500 * (0.0001/2) * 100 * 30)
print(len(chunks)) # $2250 per month using cohere

# 30 * 500 * (0.00001/2) * 100 * 30 = $225/month using amazon embed batch processing
