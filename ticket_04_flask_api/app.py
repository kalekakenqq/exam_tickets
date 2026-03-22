# установка: pip install flask
# запуск: python app.py
# тест: curl http://localhost:5000/api/notes
from flask import Flask, request, jsonify

app = Flask(__name__)

# хранение заметок в памяти (список словарей)
notes = []
next_id = 1


@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify(notes)


@app.route('/api/notes', methods=['POST'])
def create_note():
    global next_id
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'нужно поле text'}), 400
    note = {'id': next_id, 'text': data['text']}
    notes.append(note)
    next_id += 1
    return jsonify(note), 201


@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = next((n for n in notes if n['id'] == note_id), None)
    if note is None:
        return jsonify({'error': 'заметка не найдена'}), 404
    return jsonify(note)


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    global notes
    note = next((n for n in notes if n['id'] == note_id), None)
    if note is None:
        return jsonify({'error': 'заметка не найдена'}), 404
    notes = [n for n in notes if n['id'] != note_id]
    return jsonify({'message': 'удалено'})


if __name__ == '__main__':
    app.run(debug=True)
