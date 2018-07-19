#!/usr/bin/env python3


from argparse import ArgumentParser
import collections
import spacy
import sys

NLP = spacy.load('es_core_news_md')


def create_parser():
    """
    Settings for argparse
    """

    parser = ArgumentParser(description='Convert TXT document into CWB Format')

    parser.add_argument(
        '--input',
        help='Input TXT file to convert to CWB',
        dest='input',
        required=True)

    return parser


def create_document(lines_of_document):
    """
    Returns tuple for headline and body.
    """

    Document = collections.namedtuple('Document', ['header', 'body'])
    document = Document(body=' '.join(lines_of_document[1:]),
                        header=lines_of_document[0])

    return document


def create_document_list(lines_of_file):
    """
    Creates a list of Document tuples from all the lines of a file.
    """

    document = []
    documents = []

    for line in lines_of_file:
        document.append(line.rstrip())

        # Either a newline of the last line
        if line == '\n' or line == lines_of_file[-1]:
            documents.append(create_document(document))
            document = []

    return documents


def print_cwb(document, tag='<s>'):
    """
    Annotates and prints the sentences in CQP format
    """

    doc = NLP(document)
    for sentence in doc.sents:
        print(tag)

        sent = NLP(sentence.text)
        for token in sent:
            print('{word}\t{pos}\t{lemma}'.format(
                word=token.text,
                pos=token.pos_,
                lemma=token.lemma_))

        print(tag.replace('<', '</'))


def print_header(filename):
    """
    Prints document head with its attributes
    Input should be like: 2017_11_03_example-text.txt
    """

    date_list = filename[0:10].split('_')
    # Hint: CWB Metadata cannot contain dashes -
    name = 'id="{}"'.format(filename[0:-4].replace('-', '_'))
    date = 'date="{}"'.format('_'.join(date_list))
    year = 'year="{}"'.format(date_list[0])
    month = 'month="{}"'.format(date_list[1])
    day = 'day="{}"'.format(date_list[2])

    header = '<text {} {} {} {} {}>'.format(name, date, year, month, day)

    print(header)

def print_footer():
    """
    Prints end of document. Just for symmetry.
    """
    print('</text>')


def main(argsparser):
    """
    Entrypoint
    """

    args = argsparser.parse_args()
    filepath = args.input
    filename = args.input.split('/')[-1]

    try:
        encoding = 'utf-8'
        input_doc = open(filepath,  encoding=encoding)
        lines = input_doc.readlines()
    except UnicodeDecodeError:
        encoding = 'cp1252'
        input_doc = open(filepath,  encoding=encoding)
        lines = input_doc.readlines()
    except UnicodeDecodeError:
        print('Could not convert file: {}'.format(filename), file=sys.stderr)
        sys.exit(1)
    finally:
        input_doc.close()
        documents = create_document_list(lines)

    for doc in documents:
        print_header(filename)
        print_cwb(doc.header, tag='<h1>')
        print_cwb(doc.body)
        print_footer()


if __name__ == '__main__':

    CMDARGS = create_parser()
    main(CMDARGS)
