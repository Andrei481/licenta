import nltk

file_path = '../data/text.txt'
text = ""

with open(file_path, 'r', encoding='utf-8') as file:
    text = file.readlines()  # Read lines instead of the entire text

nltk.download('punkt')
sentence_delims = ['.', '!', '?']
pairs = []

def text_to_input_output(line, input_size=50, output_size=10):
    words = nltk.word_tokenize(line)
    line_pairs = []

    if len(words) >= input_size + output_size:
        for i in range(len(words) - input_size - output_size + 1):
            context = words[i:i + input_size]
            target = words[i + input_size:i + input_size + output_size]

            # Extend target until a sentence delimiter is found or the end of the text
            while target[-1] not in sentence_delims and len(target) < len(words[i + input_size:]):
                target.append(words[i + input_size + len(target)])

            input_text = ' '.join(context)
            output_text = ' '.join(target)

            line_pairs.append({'input': input_text, 'output': output_text})

    return line_pairs

for line in text:
    line_pairs = text_to_input_output(line)
    pairs.extend(line_pairs)

# Print each pair on a separate line
for pair in pairs:
    print(f"Input: {pair['input']}\n")
    print(f"Output: {pair['output']}\n")
