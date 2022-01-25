# -*- coding: utf-8 -*-
# file: translator.py
# time: 2021/8/6
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import os
import random
from collections import defaultdict, Counter

import onmt
import torch
from autocuda import auto_cuda_index
from findfile import find_file, find_dir
from onmt.bin.build_vocab import build_vocab_main
from onmt.inputters.inputter import _load_vocab, _build_fields_vocab, get_fields
from onmt.opts import dynamic_prepare_opts
from onmt.translate import GNMTGlobalScorer, Translator
from onmt.utils.misc import set_random_seed
from onmt.utils.parse import ArgumentParser
from torch import nn
from torchtext.data import Example

from DaNuoYi import global_config


class InjectionTranslator:
    def __init__(self, source_task, target_task):
        self.source_task = source_task
        self.target_task = target_task
        state_dict_path = find_dir(global_config.PROJECT_PATH, ['translation_datasets', '{}2{}'.format(source_task, target_task)])

        is_cuda = torch.cuda.is_available()
        set_random_seed(1111, is_cuda)

        src_vocab_path = "{}/vocab.src".format(state_dict_path)
        tgt_vocab_path = "{}/vocab.tgt".format(state_dict_path)

        src_val = find_file(global_config.PROJECT_PATH, ["{}2{}".format(source_task, target_task), "src-val.txt"])
        tgt_val = find_file(global_config.PROJECT_PATH, ["{}2{}".format(source_task, target_task), "tgt-val.txt"])

        src_data = {"reader": onmt.inputters.str2reader["text"](), "data": src_val}
        tgt_data = {"reader": onmt.inputters.str2reader["text"](), "data": tgt_val}
        self._readers, self._data = onmt.inputters.Dataset.config(
            [('src', src_data)])

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

        gpu = int(auto_cuda_index())
        self.device = 'cuda:{}'.format(gpu) if torch.cuda.is_available() else -1

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
        if not state_dict_path:
            os.makedirs(state_dict_path)

        # yaml_config = """
        #        ## Where the vocab(s) will be written
        #        src_vocab: {0}/runtime_materials/translation_datasets/{1}2{2}/vocab.src
        #        tgt_vocab: {0}/runtime_materials/translation_datasets/{1}2{2}/vocab.tgt
        #        # Prevent overwriting existing files in the folder
        #        save_data: {0}/runtime_materials/translation_datasets/{1}2{2}/
        #        # Corpus opts:
        #        data:
        #          corpus_1:
        #            path_src: {0}/runtime_materials/translation_datasets/{1}2{2}/src-train.txt
        #            path_tgt: {0}/runtime_materials/translation_datasets/{1}2{2}/tgt-train.txt
        #          valid:
        #            path_src: {0}/runtime_materials/translation_datasets/{1}2{2}/src-val.txt
        #            path_tgt: {0}/runtime_materials/translation_datasets/{1}2{2}/tgt-val.txt
        #        """.format(global_config.PROJECT_PATH, source_task, target_task)
        # with open('{0}/runtime_materials/translation_datasets/{1}2{2}/{1}2{2}_config.yaml'.format(
        #         global_config.PROJECT_PATH, source_task, target_task), "w") as f:
        #     f.write(yaml_config)
        # parser = ArgumentParser(description='build_vocab.py')
        # dynamic_prepare_opts(parser, build_vocab_only=True)
        #
        # base_args = (["-config",
        #               find_file(global_config.PROJECT_PATH, "{}2{}_config.yaml".format(source_task, target_task)),
        #               "-overwrite",
        #               "-n_sample", "10000"])
        #
        # opts, unknown = parser.parse_known_args(base_args)
        #
        # build_vocab_main(opts)

        is_cuda = torch.cuda.is_available()
        set_random_seed(1111, is_cuda)


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
        model = onmt.models.model.NMTModel(encoder, decoder)
        model.to(self.device)
        # Specify the tgt word generator and loss computation module
        model.generator = nn.Sequential(
            nn.Linear(rnn_size, len(tgt_vocab)),
            nn.LogSoftmax(dim=-1)).to(self.device)

        state_dict_path = find_file(global_config.PROJECT_PATH, ['{}2{}'.format(source_task, target_task), 'state_dict'])
        state_dict = torch.load(state_dict_path, map_location=self.device)
        model.load_state_dict(state_dict)
        # initialize fields
        src_nfeats, tgt_nfeats = 0, 0  # do not support word features for now
        fields = get_fields(
            'text', src_nfeats, tgt_nfeats)

        self.vocab_fields = _build_fields_vocab(
            fields, counters, 'text', share_vocab,
            vocab_size_multiple,
            src_vocab_size, src_words_min_frequency,
            tgt_vocab_size, tgt_words_min_frequency)

        self.src_text_field = self.vocab_fields["src"].base_field
        self.src_vocab = self.src_text_field.vocab

        self.tgt_text_field = self.vocab_fields['tgt'].base_field
        self.tgt_vocab = self.tgt_text_field.vocab

        self.builder = None
        self.data_iter = None

        self.fields = {k: [(k, v)] for k, v in self.vocab_fields.items()}

        self.dataset = onmt.inputters.Dataset(
            self.vocab_fields, readers=self._readers, data=self._data,
            sort_key=onmt.inputters.str2sortkey["text"])

        self.src_reader = onmt.inputters.str2reader["text"]
        self.tgt_reader = onmt.inputters.str2reader["text"]
        scorer = GNMTGlobalScorer(alpha=0.7,
                                  beta=0.,
                                  length_penalty="avg",
                                  coverage_penalty="none")

        self.translator = Translator(model=model,
                                     fields=self.vocab_fields,
                                     src_reader=self.src_reader,
                                     tgt_reader=self.tgt_reader,
                                     global_scorer=scorer,
                                     gpu=gpu)

        # self.f_translated = open(find_file(global_config.PROJECT_PATH,
        #                                    '{}.txt'.format(self.target_task)
        #                                    ).replace('.txt', '.translated.{}.txt'.format(random.randint(0, 10000))),
        #                          mode='a+',
        #                          encoding='utf8'
        #                          )

    def translate(self, source_injection: str):
        self.dataset.examples = [Example.fromdict({'src': source_injection, 'tgt': source_injection, 'indices': 0}, self.fields)]
        self.builder = onmt.translate.TranslationBuilder(data=self.dataset, fields=self.vocab_fields)

        self.data_iter = onmt.inputters.OrderedIterator(
            dataset=self.dataset,
            device=self.device,
            batch_size=1,
            train=False,
            sort=False,
            sort_within_batch=True,
            shuffle=False
        )

        for batch in self.data_iter:
            trans_batch = self.translator.translate_batch(
                batch=batch, src_vocabs=[self.src_vocab],
                attn_debug=False)
            translations = self.builder.from_batch(trans_batch)

            # self.f_translated.write(' '.join(translations[0].pred_sents[0]) + '\n')
            # print(' '.join(translations[0].pred_sents[0]) + '\n')

            return ' '.join(translations[0].pred_sents[0])
