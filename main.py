import re
import nltk
import pdfplumber
import math
import json

def prepare_to_JSONL(values, section_name):
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

def format_data_from_text(extracted_text, sections):
    section = {'name': '', 'values': []}
    prev_title = ''
    curr_title = ''
    for line in extracted_text:
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

    return section

def main():
    files = ["./test.pdf", "./test2.pdf", "./test3.pdf", "./test4.pdf", "./test5.pdf"]
    pdf_file = pdfplumber.open('./test2.pdf')

    sections = []
    for p, char in zip(pdf_file.pages, pdf_file.chars):

        width = p.width
        height = p.height

        first_half_x = width / 2
        second_half_x = width - first_half_x

        # to make it easier to extract the data, we split the pdf page into two halves along the y axis and extract page by page
        cropped = p.crop((0, 0, first_half_x, height))
        cropped2 = p.crop((second_half_x, 0, width, height))

        # skip first page since does not contain actual useful data (apart from aircraft info which might be useful later)
        if p.page_number < 2:
            continue

        # extract left half of page
        extracted = cropped.extract_text_lines()

        #extract right half of page
        extracted2 = cropped2.extract_text_lines()

        format_data_from_text(extracted, sections)
        format_data_from_text(extracted2, sections)

    pdf_file.close()

    data_for_training = []
    for section in sections:
        data_for_training.append(prepare_to_JSONL(section['values'], section['name']))

    with open('training.json', "w") as text_file:
        for item in data_for_training:
            for line in item:
                text_file.write(json.dumps(line))
                text_file.write("\n")
        

if __name__ == "__main__":
    main()