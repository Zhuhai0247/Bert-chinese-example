import paddlehub as hub



label_map = ['ebook', 'fullvplay', 'loccity', 'login', 'logintext', 'map',
                'mediaedit', 'mine', 'negative', 'permission', 'policydetail',
                'privacypolicy', 'realauth', 'rentindex', 'shopdetail', 'shoplist',
                'takephoto', 'topiclist', 'travelsearch', 'videolist', 'youngmode']

model = hub.Module(
    name='chinese-bert-wwm',
    task='seq-cls',
    load_checkpoint='D:\\SaveMe\\best_model\\model.pdparams',
    label_map=label_map)
results = model.predict(data, max_seq_len=128, batch_size=1, use_gpu=True)
for idx, texts in enumerate(data):
    print('TextA: {}\t Label: {}'.format(texts[0], results[idx]))
