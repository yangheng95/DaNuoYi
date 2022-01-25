# -*- coding: utf-8 -*-
# file: train_translator.py
# time: 2021/8/6
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

# -*- coding: utf-8 -*-
# file: demo.py
# time: 2021/8/1
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os
from collections import defaultdict, Counter

import onmt
import torch
import torch.nn as nn
from autocuda import auto_cuda_index
from findfile import find_file, find_dir
from onmt.bin.build_vocab import build_vocab_main
from onmt.inputters.corpus import ParallelCorpus
from onmt.inputters.dynamic_iterator import DynamicDatasetIter
from onmt.inputters.inputter import _load_vocab, _build_fields_vocab, get_fields, IterOnDevice
from onmt.opts import dynamic_prepare_opts
from onmt.utils.logging import init_logger
from onmt.utils.misc import set_random_seed
from onmt.utils.parse import ArgumentParser

from DaNuoYi import global_config


class InjectionTranslatorTrainer:
    def __init__(self, source_task, target_task):
        cuda_index = auto_cuda_index()

        dataset_path = find_dir(global_config.PROJECT_PATH, ['translation_datasets', '{}2{}'.format(task1, task2)])
        state_dict_path = os.path.join(global_config.PROJECT_PATH, 'runtime_materials/translation_datasets/{}2{}'.format(task1, task2))
        if not state_dict_path:
            os.makedirs(state_dict_path)

        yaml_config = """
        ## Where the vocab(s) will be written
        src_vocab: {0}/runtime_materials/translation_datasets/{1}2{2}/vocab.src
        tgt_vocab: {0}/runtime_materials/translation_datasets/{1}2{2}/vocab.tgt
        # Prevent overwriting existing files in the folder
        save_data: {0}/runtime_materials/translation_datasets/{1}2{2}/
        # Corpus opts:
        data:
          corpus_1:
            path_src: {0}/runtime_materials/translation_datasets/{1}2{2}/src-train.txt
            path_tgt: {0}/runtime_materials/translation_datasets/{1}2{2}/tgt-train.txt
          valid:
            path_src: {0}/runtime_materials/translation_datasets/{1}2{2}/src-val.txt
            path_tgt: {0}/runtime_materials/translation_datasets/{1}2{2}/tgt-val.txt
        """.format(global_config.PROJECT_PATH, source_task, target_task)
        with open('{0}/runtime_materials/translation_datasets/{1}2{2}/{1}2{2}_config.yaml'.format(
                      global_config.PROJECT_PATH, source_task, target_task), "w") as f:
            f.write(yaml_config)
        parser = ArgumentParser(description='build_vocab.py')

        init_logger()

        is_cuda = torch.cuda.is_available()
        set_random_seed(1111, is_cuda)

        dynamic_prepare_opts(parser, build_vocab_only=True)

        base_args = (["-config",
                      find_file(global_config.PROJECT_PATH, "{}2{}_config.yaml".format(task1, task2)),
                      "-overwrite",
                      "-n_sample", "10000"])

        opts, unknown = parser.parse_known_args(base_args)

        build_vocab_main(opts)

        src_vocab_path = "{}/vocab.src".format(state_dict_path)
        tgt_vocab_path = "{}/vocab.tgt".format(state_dict_path)

        # initialize the frequency counter
        counters = defaultdict(Counter)
        # load source vocab
        _src_vocab, _src_vocab_size = _load_vocab(
            src_vocab_path,
            'src',
            counters)
        # load target vocab
        _tgt_vocab, _tgt_vocab_size = _load_vocab(
            tgt_vocab_path,
            'tgt',
            counters)

        # initialize fields
        src_nfeats, tgt_nfeats = 0, 0  # do not support word features for now
        fields = get_fields(
            'text', src_nfeats, tgt_nfeats)

        # build fields vocab
        share_vocab = False
        vocab_size_multiple = 1
        src_vocab_size = 300
        tgt_vocab_size = 300
        src_words_min_frequency = 1
        tgt_words_min_frequency = 1
        vocab_fields = _build_fields_vocab(
            fields, counters, 'text', share_vocab,
            vocab_size_multiple,
            src_vocab_size, src_words_min_frequency,
            tgt_vocab_size, tgt_words_min_frequency)

        src_text_field = vocab_fields["src"].base_field
        src_vocab = src_text_field.vocab
        src_padding = src_vocab.stoi[src_text_field.pad_token]

        tgt_text_field = vocab_fields['tgt'].base_field
        tgt_vocab = tgt_text_field.vocab
        tgt_padding = tgt_vocab.stoi[tgt_text_field.pad_token]

        ##########################################################################  Model
        emb_size = 100
        rnn_size = 100
        # Specify the core model.

        encoder_embeddings = onmt.modules.Embeddings(emb_size, len(src_vocab),
                                                     word_padding_idx=src_padding)

        encoder = onmt.encoders.RNNEncoder(hidden_size=rnn_size, num_layers=1,
                                           rnn_type="LSTM", bidirectional=True,
                                           embeddings=encoder_embeddings)

        decoder_embeddings = onmt.modules.Embeddings(emb_size, len(tgt_vocab),
                                                     word_padding_idx=tgt_padding)
        decoder = onmt.decoders.decoder.InputFeedRNNDecoder(
            hidden_size=rnn_size, num_layers=1, bidirectional_encoder=True,
            rnn_type="LSTM", embeddings=decoder_embeddings)
        device = torch.device(cuda_index) if torch.cuda.is_available() else "cpu"
        model = onmt.models.model.NMTModel(encoder, decoder)
        model.to(device)

        # Specify the tgt word generator and loss computation module
        model.generator = nn.Sequential(
            nn.Linear(rnn_size, len(tgt_vocab)),
            nn.LogSoftmax(dim=-1)).to(device)

        loss = onmt.utils.loss.NMTLossCompute(
            criterion=nn.NLLLoss(ignore_index=tgt_padding, reduction="sum"),
            generator=model.generator)

        lr = 0.001
        torch_optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        optim = onmt.utils.optimizers.Optimizer(
            torch_optimizer, learning_rate=lr, max_grad_norm=2)

        src_train = find_file(global_config.PROJECT_PATH, ["{}2{}".format(source_task, target_task), "src-train.txt"])
        tgt_train = find_file(global_config.PROJECT_PATH, ["{}2{}".format(source_task, target_task), "tgt-train.txt"])

        src_val = find_file(global_config.PROJECT_PATH, ["{}2{}".format(source_task, target_task), "src-val.txt"])
        tgt_val = find_file(global_config.PROJECT_PATH, ["{}2{}".format(source_task, target_task), "tgt-val.txt"])

        # build the ParallelCorpus
        corpus = ParallelCorpus("corpus", src_train, tgt_train)
        valid = ParallelCorpus("valid", src_val, tgt_val)

        # build the training iterator
        train_iter = DynamicDatasetIter(
            corpora={"corpus": corpus},
            corpora_info={"corpus": {"weight": 1}},
            transforms={},
            fields=vocab_fields,
            is_train=True,
            batch_type="tokens",
            batch_size=4096,
            batch_size_multiple=1,
            data_type="text")

        # make sure the iteration happens on GPU 0 (-1 for CPU, N for GPU N)
        train_iter = iter(IterOnDevice(train_iter, cuda_index))

        # build the validation iterator
        valid_iter = DynamicDatasetIter(
            corpora={"valid": valid},
            corpora_info={"valid": {"weight": 1}},
            transforms={},
            fields=vocab_fields,
            is_train=False,
            batch_type="sents",
            batch_size=8,
            batch_size_multiple=1,
            data_type="text")

        valid_iter = IterOnDevice(valid_iter, cuda_index)

        report_manager = onmt.utils.ReportMgr(
            report_every=50, start_time=None, tensorboard_writer=None)

        trainer = onmt.Trainer(model=model,
                               train_loss=loss,
                               valid_loss=loss,
                               optim=optim,
                               report_manager=report_manager,
                               dropout=[0.1])

        trainer.train(train_iter=train_iter,
                      train_steps=1000,
                      valid_iter=valid_iter,
                      valid_steps=500)

        save_path = os.path.join(global_config.PROJECT_PATH,
                                 'runtime_materials/translation_datasets/{}2{}'.format(source_task, target_task))
        if not save_path:
            os.makedirs(save_path)

        torch.save(model.state_dict(), os.path.join(save_path, 'translator.state_dict'))

        # model.to(cuda_index)

        # # Translate test
        # src_data = {"reader": onmt.inputters.str2reader["text"](), "data": src_val}
        # tgt_data = {"reader": onmt.inputters.str2reader["text"](), "data": tgt_val}
        # _readers, _data = onmt.inputters.Dataset.config(
        #     [('src', src_data), ('tgt', tgt_data)])
        #
        # dataset = onmt.inputters.Dataset(
        #     vocab_fields, readers=_readers, data=_data,
        #     sort_key=onmt.inputters.str2sortkey["text"])
        #
        # data_iter = onmt.inputters.OrderedIterator(
        #     dataset=dataset,
        #     device="cuda:{}".format(cuda_index),
        #     batch_size=10,
        #     train=False,
        #     sort=False,
        #     sort_within_batch=True,
        #     shuffle=False
        # )
        #
        # src_reader = onmt.inputters.str2reader["text"]
        # tgt_reader = onmt.inputters.str2reader["text"]
        # scorer = GNMTGlobalScorer(alpha=0.7,
        #                           beta=0.,
        #                           length_penalty="avg",
        #                           coverage_penalty="none")
        # translator = Translator(model=model,
        #                         fields=vocab_fields,
        #                         src_reader=src_reader,
        #                         tgt_reader=tgt_reader,
        #                         global_scorer=scorer,
        #                         gpu=cuda_index)
        # builder = onmt.translate.TranslationBuilder(data=dataset,
        #                                             fields=vocab_fields)
        #
        # for batch in data_iter:
        #     trans_batch = translator.translate_batch(
        #         batch=batch, src_vocabs=[src_vocab],
        #         attn_debug=False)
        #     translations = builder.from_batch(trans_batch)
        #     for trans in translations:
        #         print(trans.log(0))


if __name__ == '__main__':
    injection_tasks = ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]
    # injection_tasks = ["xmli", "xss"]

    for task1 in injection_tasks:
        for task2 in injection_tasks:
            if task1 != task2:
                InjectionTranslatorTrainer(task1, task2)
