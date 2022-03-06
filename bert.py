import paddle
import paddlehub as hub
from paddlehub.datasets.base_nlp_dataset import TextClassificationDataset


class MyDataset(TextClassificationDataset):
    # 数据集存放目录
    base_path = 'D:\\SaveMe\\data_dir\\'
    # 数据集的标签列表
    label_list=['ebook', 'fullvplay', 'loccity', 'login', 'logintext', 'map',
                'mediaedit', 'mine', 'negative', 'permission', 'policydetail',
                'privacypolicy', 'realauth', 'rentindex', 'shopdetail', 'shoplist',
                'takephoto', 'topiclist', 'travelsearch', 'videolist', 'youngmode']


    def __init__(self, tokenizer, max_seq_len: int = 128, mode: str = 'train'):
        if mode == 'train':
            data_file = 'train.txt'
        elif mode == 'test':
            data_file = 'test.txt'
        else:
            data_file = 'dev.txt'
        super().__init__(
            base_path=self.base_path,
            tokenizer=tokenizer,
            max_seq_len=max_seq_len,
            mode=mode,
            data_file=data_file,
            label_list=self.label_list,
            is_file_with_header=True)


# 选择所需要的模型，获取对应的tokenizer
model = hub.Module(name='chinese-bert-wwm-ext', task='seq-cls', num_classes=len(MyDataset.label_list))
tokenizer = model.get_tokenizer()

# 实例化训练集
train_dataset = MyDataset(tokenizer,mode='train')
dev_dataset = MyDataset(tokenizer,mode='dev')
test_dataset = MyDataset(tokenizer,mode='test')

#优化器
optimizer = paddle.optimizer.AdamW(learning_rate=5e-5, parameters=model.parameters())
trainer = hub.Trainer(model, optimizer, checkpoint_dir='./', use_gpu=True)


trainer.train(
    train_dataset,
    epochs=10,
    batch_size=16,
    eval_dataset=dev_dataset,
    save_interval=2,
)

trainer.evaluate(test_dataset, batch_size=16)
