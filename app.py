from flask import Flask, request, jsonify

app = Flask(__name__)

# Dữ liệu giả định từ vector storage và backup files
vector_storage = {
    "vs_nAzICCslyhFBaeZaKQK6B9dx": {
        "Passage 1": "Nội dung của Passage 1 từ vector storage...",
        "Passage 2": "Nội dung của Passage 2 từ vector storage...",
    }
}

backup_files_data = {
    "file-7LK0OPinER4ox3CZMRGhBgdi": {
        "Passage 1": "Nội dung của Passage 1 từ file-7LK0OPinER4ox3CZMRGhBgdi...",
        "Passage 2": "Nội dung của Passage 2 từ file-7LK0OPinER4ox3CZMRGhBgdi...",
        "Passage 3": "Nội dung của Passage 3 từ file-7LK0OPinER4ox3CZMRGhBgdi..."
    }
}

def retrieve_data_from_vector_storage(vector_id):
    return vector_storage.get(vector_id, {})

def retrieve_data_from_backup_files():
    data = {}
    for file_id, passages in backup_files_data.items():
        for passage_id, content in passages.items():
            if passage_id not in data:
                data[passage_id] = content
    return data

def get_passage_content(data, user_choice):
    if user_choice in ["passage 1", "passage 2", "passage 3"]:
        return data.get(user_choice.title(), "Không tìm thấy nội dung cho passage này.")
    elif user_choice == "cả 3":
        return "\n\n".join([data[p] for p in ["Passage 1", "Passage 2", "Passage 3"] if p in data])
    else:
        return "Lựa chọn không hợp lệ. Vui lòng thử lại."

@app.route('/function_call', methods=['POST'])
def function_call():
    data = request.get_json()
    function_name = data.get('name')
    arguments = data.get('arguments', {})
    
    if function_name == "retrieve_latest_reading":
        request_param = arguments.get("request")
        user_choice = arguments.get("user_choice").lower()
        data = retrieve_data_from_vector_storage("vs_nAzICCslyhFBaeZaKQK6B9dx")
        
        if len(data) < 3:
            data = retrieve_data_from_backup_files()

        content = get_passage_content(data, user_choice)
        
        return jsonify({
            "name": function_name,
            "response": {
                "content": content
            }
        })

    return jsonify({"error": "Function call not supported"}), 400

if __name__ == '__main__':
    app.run(debug=True)
