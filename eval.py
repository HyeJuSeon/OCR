def replace(str):
    str = str[:-7].strip()
    return str.replace('간판_가로형간판', '간판_가로형간판')

def pred_file_preprocessing():
    with open('log_eval_result.txt', 'r', encoding='utf-8') as f:
        file = f.readlines()
    file = [line for line in file if 'test' in line]
    file = list(map(replace, file))
    return file

def eval_log():
    '''
    label: test/간판_가로형간판_161805_0.jpg	죠다쉬 세이프티
    pred: /content/gdrive/MyDrive/ocr/data/test/간판_가로형간판_151464_0.jpg	믿음                       	0.9615
    '''
    with open('gt_test.txt', 'r') as f:
         label_file = f.readlines()
    pred_file = pred_file_preprocessing()
    label_dict = dict()
    pred_dict = dict()
    files = set()
    for label_line, pred_line in zip(label_file, pred_file):
        file, label = label_line.split('\t')
        idx = file.find('간')
        label_dict[file[idx:]] = label.strip()
        files.add(file[idx:])
        try:
            file, pred = pred_line.strip().split('\t')
        except:
            file = pred_line.strip()
            pred = ' '
        idx = file.find('간')
        pred_dict[file[idx:]] = pred

    correct = 0
    for file in list(files):
        if pred_dict[file] == label_dict[file]:
            correct += 1
    print(f'Test accuracy: {correct / len(files):0.4f}')

def eval():
    '''
    label: test/간판_가로형간판_161805_0.jpg	죠다쉬 세이프티
    pred: /content/gdrive/MyDrive/ocr/data/test/간판_가로형간판_151464_0.jpg	믿음
    '''
    with open('gt_test.txt', 'r') as f:
         label_file = f.readlines()
    with open('eval_result.txt', 'r') as f:
         pred_file = f.readlines()
    label_dict = dict()
    pred_dict = dict()
    files = []
    for label_line, pred_line in zip(label_file, pred_file):
        file, label = label_line.strip().split('\t')
        idx = file.find('간')
        label_dict[file[idx:]] = label
        try:
            file, pred = pred_line.strip().split('\t')
        except:
            file = pred_line.strip()
            pred = ' '
        idx = file.find('간')
        pred_dict[file[idx:]] = pred
        files.append(file[idx:])

    correct = 0
    for file in list(files):
        if pred_dict[file] == label_dict[file]:
            correct += 1
    print(f'Test accuracy: {correct / len(files):0.4f}')

if __name__ == '__main__':
    eval_log()
