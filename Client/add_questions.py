from pymongo import MongoClient

client = MongoClient()
db = client.student_modeling
collection = db.questions

while True:
    concept = input('Enter the concept name: ')
    question = input('Enter the question: ')
    A = input('Enter option A: ')
    B = input('Enter option B: ')
    C = input('Enter option C: ')
    D = input('Enter option D: ')
    options = [A, B, C, D]
    answer = int(input('Enter the right answer (0-based integer): '))

    document = {
        'question': question,
        'options': options,
        'answer': answer,
        'concept': concept
    }

    result = collection.insert_one(document)
    print('Successfully added. Document id:', result.inserted_id)
    
    cont = input('Continue? (Y/N): ')
    if cont == 'N' or cont == 'n':
        break
    else:
        print()

print('Done.')
