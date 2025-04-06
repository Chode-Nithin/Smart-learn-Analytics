import pdfplumber
import pandas as pd


def extract_questions_from_pdf(pdf_file):
    questions = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            print("------------page", text)
            # Split the text into individual questions based on the numbering pattern
            split_text = text.split('\n')
            print("-----------questions", split_text)
            question = ''
            options = []
            correct_answer = ''
            for line in split_text:
                if line.strip().startswith('Correct Answer:'):
                    correct_answer = line.strip().split(':')[-1].strip()
                    break
                if line.strip().startswith(('A)', 'B)', 'C)', 'D)')):
                    options.append(line.strip())
                else:
                    question += line.strip() + ' '

            questions.append({
                'question': question.strip(),
                'option_A': options[0] if len(options) > 0 else '',
                'option_B': options[1] if len(options) > 1 else '',
                'option_C': options[2] if len(options) > 2 else '',
                'option_D': options[3] if len(options) > 3 else '',
                'correct_answer': correct_answer.split(')')[1].strip() if correct_answer else ''
            })
        print("------------questions", questions)
    print(questions)
    return questions


def write_to_excel(questions, excel_file):
    df = pd.DataFrame(questions)
    print(df)
    df['id'] = df.index + 1
    df = df[['id', 'question', 'option_A', 'option_B', 'option_C',
             'option_D', 'difficulty', 'skill', 'correct_answer']]
    df.to_excel(excel_file, index=False)


if __name__ == "__main__":
    pdf_file = 'WEB DEVELOPMENT_Test1.pdf'
    excel_file = 'Book1.xlsx'

    questions = extract_questions_from_pdf(pdf_file)
    write_to_excel(questions, excel_file)
