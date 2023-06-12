import re
import nltk
from PyPDF2 import PdfReader
import pdfplumber
import math

def read_PDF(file):
    reader = PdfReader(file)
    num_of_pages = len(reader.pages)

    page = reader.pages[0]
    text = page.extract_text()

    # print(text)
    return text


# There's an issue here where some of the checklist sections don't get properly split because they are in the same line as the item. may require manual fixing of this here (review)
def parse_PDF(text):
    result = []

    bullet_point = re.compile(r"\u2022")
    last_title_idx = 0

    lines = text.split('\n')
    curr = []

    regex = "^[A-Z ]*$"
    for idx, line in enumerate(lines):
        if (re.search(bullet_point, line)):
            res = line.strip()
            cleanString = re.sub(bullet_point, '', res)

            test = cleanString

            curr.append(test)   
        else:
            regex = "^[A-Z ]*$"
            test = bool(re.search(regex, line))
            if is_valid_token(line) and test:
                result.append({"name": lines[last_title_idx].strip(), "values": curr})
                last_title_idx = idx
                curr = []

    return result

def is_valid_token(token):
    return token and token.strip()

def is_upper(string):
    return string.isupper() and string.isalpha()


def rearrenge_tokens(values, section_name):
    res = []

    for idx, item in enumerate(values):
        curr = {'prompt': '', 'completion': ''}

        if idx == 0:
            curr['prompt'] = section_name # ask for title of the current checklist
            curr['completion'] = item['q'] # responds the prompt to the first question
        elif idx == len(values):
            curr['prompt'] = values[idx]['a'] # ask for the last answer of the current checklist
            curr['completion'] = section_name + 'COMPLETED' # responds with checklist completion
        else:
            curr['prompt'] = values[idx -1]['a'] # ask for the last answer we gave
            curr['completion'] = item['q'] # responds with the next checklist item

        res.append(curr)
    return res

def extract_title(text):
    title = ''
    for ch in text['chars']:
                if ch['non_stroking_color'] == [1, 0, 0]:
                    # save the current title somewhere
                    is_title = True
                    title = text['text']
                    break
    return title

def extract_key_values(text):
    regex = "^[A-Z0-9!@#$%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>\\/?]*$"
    tokenized = nltk.word_tokenize(text['text'])

    q = ''
    a = ''
    for w in tokenized:
        if bool(re.search(regex, w)):
            a += w + " "
        else:
            q += w + " "

    return {'q': q, 'a': a}

def main():
    files = ["./test.pdf", "./test2.pdf", "./test3.pdf", "./test4.pdf", "./test5.pdf"]
    pdf_file = pdfplumber.open('./test2.pdf')


    sections = []
    for p, char in zip(pdf_file.pages, pdf_file.chars):
        # texts = p.extract_tables({'vertical_strategy': 'text', 'horizontal_strategy': 'text', "text_tolerance": 10})
        width = p.width
        height = p.height

        first_half_x = width / 2
        first_half_y = height / 2

                        #x0, top, x1, bottom
        cropped = p.crop((0, 0, first_half_x, height))


        # skip first page since does not contain actual ch
        if p.page_number < 2:
            continue

        extracted = cropped.extract_text_lines()

        section = {'name': '', 'values': []}
        prev_title = ''
        curr_title = ''
        for line in extracted:
            
            title = extract_title(line)
            if title:
                curr_title = title
                section = {'name': curr_title, 'values': []}
            else:
                if prev_title != curr_title:
                    sections.append(section)
                    prev_title = curr_title

                key_val = extract_key_values(line)
                section['values'].append(key_val)

        # sections.append(section)
    

if __name__ == "__main__":
    main()