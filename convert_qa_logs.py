import json

def format_log_entry(entry):
    formatted_entry = []
    formatted_entry.append(f"Question: {entry['question']}")
    formatted_entry.append(f"Question Time: {entry['question_time']}")
    formatted_entry.append("Response:")
    formatted_entry.append(json.dumps(entry['response'], indent=4, ensure_ascii=False))
    formatted_entry.append(f"Response Time: {entry['response_time']}")
    formatted_entry.append(f"Latency (ms): {entry['latency_ms']:.2f}")
    return "\n".join(formatted_entry)

def process_logs(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            entry = json.loads(line.strip())
            formatted_entry = format_log_entry(entry)
            outfile.write(formatted_entry + "\n\n" + "="*27 + "\n\n")

process_logs('qa_logs.txt', 'qo_logs_hw.txt')
