import linguistica as lxa
import pprint

lxa_object = lxa.read_corpus('linguistica/datasets/Arabic.dx1', max_word_tokens=50000)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(lxa_object.stems())
