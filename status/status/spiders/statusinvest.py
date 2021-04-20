import scrapy
import json
from math import sqrt
from ..items import StatusItem
from ..config import API
from pprint import pprint

from scraper_api import ScraperAPIClient
client = ScraperAPIClient(API)


class StatusinvestSpider(scrapy.Spider):
    name = 'statusinvest'

    setoresLista = [
        'indice-de-consumo',
        'indice-carbono-eficiente',
        'indice-de-energia-eletrica',
        'indice-financeiro',
        'indice-de-materiais-basicos',
        'indice-imobiliario',
        'indice-do-setor-industrial',
        'indice-utilidade-publica',
        'indice-small-cap',
        'indice-midlarge-cap',
        'indice-valor',
        'indice-de-acoes-com-tag-along-diferenciado',
        'indice-de-sustentabilidade-empresarial',
        'indice-de-governanca-corporativa-–-novo-mercado',
        'indice-de-acoes-com-governanca-corporativa-diferenciada',
        'indice-de-governanca-corporativa-trade',
        'indice-brasil-50',
        'indice-brasil-100',
        'indice-brasil-amplo',
        'indice-small-cap',
        'indice-dividendos'
    ]
    setores = []
    empresaB3 = []
    start_urls = [
        'https://statusinvest.com.br/acoes/busca-avancada'
        # client.scrapyGet('https://statusinvest.com.br/acoes/busca-avancada')
    ]

    def parse(self, response):
        setor_url = "https://www.infomoney.com.br/cotacoes/empresas-b3/"

        # yield scrapy.Request(client.scrapyGet(setor_url), callback=self.parse_empresas)
        yield scrapy.Request(setor_url, callback=self.parse_empresas)

    def parse_empresas(self, response):

        url = "https://statusinvest.com.br/category/advancedsearchresult?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%220%3B25%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22peg_Ratio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22vpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorMercado%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=1"

        dic_setores_b3 = {}
        dic_setores_b3['BensIndustriais'] = response.css(
            "#bens_industriais a::text").getall()
        dic_setores_b3['ConsumoCiclico'] = response.css(
            "#consumo-ciclico a::text").getall()
        dic_setores_b3['ConsumoNaoCiclico'] = response.css(
            "#consumo_nao_ciclico a::text").getall()
        dic_setores_b3['Financeiro'] = response.css(
            "#financeiro a::text").getall()
        dic_setores_b3['MateriaisBasicos'] = response.css(
            "#bateriais_basicos a::text").getall()
        dic_setores_b3['Outros'] = response.css("#outros a::text").getall()
        dic_setores_b3['PetroleoGasBiocombustiveis'] = response.css(
            "#petroleo_gas_e_biocombustiveis a::text").getall()
        dic_setores_b3['Saude'] = response.css("#saude a::text").getall()
        dic_setores_b3['TecnologiaInformacao'] = response.css(
            "#tecnologia_da_informacao a::text").getall()
        dic_setores_b3['Telecomunicacoes'] = response.css(
            "#telecomunicacoes a::text").getall()
        dic_setores_b3['UtilidadePublica'] = response.css(
            "#utilidade-publica a::text").getall()

        self.empresaB3.append(dic_setores_b3)

        yield scrapy.Request(url, callback=self.parse_api)

        # for setor in self.empresaB3:
        #     for s in setor.keys():
        #         # pprint(f"{s} - {setor[s]}")
        #         for st in setor[s]:
        #             if st.strip()[-1] == 'F':
        #                 print("Tem IF")
        #                 pprint(f"{s} - {st.strip()[:-1]}")

    # def parse_status(self, response):
    #     url = "https://statusinvest.com.br/category/advancedsearchresult?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%220%3B25%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22peg_Ratio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22vpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorMercado%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=1"

    #     yield scrapy.Request(url, callback=self.parse_api)

    def parse_api(self, response):
        base_url = "https://statusinvest.com.br/acoes/"
        setor_url = "https://statusinvest.com.br/acao/getaltabaixa?IndiceCode="

        raw_data = response.body
        data = json.loads(raw_data)

        for setor in self.setoresLista:
            setores_url = setor_url+setor
            yield scrapy.Request(setores_url, callback=self.parse_setores)

        for status in data:
            papel = status['ticker']
            status_url = base_url+papel
            # yield scrapy.Request(client.scrapyGet(status_url), callback=self.parse_status)
            yield scrapy.Request(status_url, callback=self.parse_status)

    def parse_setores(self, response):
        setor = []
        setor = response.url.split(sep='=')

        raw_data = response.body
        data = json.loads(raw_data)

        for dados in data:
            setoresAtivo = {}
            setoresAtivo[setor[1]] = dados['code']
            self.setores.append(setoresAtivo)

    def parse_status(self, response):
        items = StatusItem()
        ticker = response.css(".fw-900.active::text").get()
        empresa = response.css('#main-header small::text').get()
        indice = ''

        for setor in self.setores:
            for se in setor.keys():
                if ticker == setor[se]:
                    indice = se
                    # print(f"setor:{se} - ticket: {setor[se]}")

        setorBtres = ''
        for setor in self.empresaB3:
            for s in setor.keys():
                for st in setor[s]:
                    if st.strip()[-1] == 'F':
                        if ticker == st.strip()[:-1]:
                            setorBtres = s
                    else:
                        if ticker == st.strip():
                            setorBtres = s

        valorAtual = response.css('.value::text').get()
        if valorAtual.replace('.', '').replace(',', '.').replace('-', '') == '':
            valorAtual = 0
        else:
            valorAtual = float(
                valorAtual.replace('.', '').replace(',', '.'))

        minCiquentaDuaSemana = response.css(
            ".w-100+ .w-lg-20 .value::text").get()
        maxCiquentaDuaSemana = response.css(
            ".border-lg-1+ .border-lg-1 .value::text").get()
        minMes = response.css(
            ".w-100+ .border-lg-1 .justify-between .sub-value::text").get()
        maxMes = response.css(
            ".border-lg-1+ .border-lg-1 .sub-value::text").get()
        valorizacaoBaseDiaAnterior = response.css(
            ".fs-md-3 .v-align-middle::text").get()
        dy = response.css(".w-lg-20 .legend-tooltip+ .value::text").get()
        somaDyDozeMeses = response.css(
            ".border-lg-1+ .w-md-50 .sub-value::text").get()
        valorizacaoAtivoDozeMeses = response.css(
            ".w-md-50 .icon+ .value::text").get()
        valorizacaoMesAtual = response.css(
            ".w-lg-20 .justify-between .v-align-middle::text").get()
        tipoAtivo = response.css(".mb-1+ .value::text").get()

        pl = response.css(
            ".w-100:nth-child(1) .item:nth-child(2) .fw-700::text").get()
        if pl.replace('.', '').replace(',', '.').replace('-', '') == '':
            pl = 0
        else:
            pl = float(pl.replace('.', '').replace(',', '.'))

        pegRatio = response.css(
            ".item:nth-child(3) .uppercase+ .pr-2 .fw-700::text").get()
        pvp = response.css(
            ".w-lg-16_6:nth-child(4) .align-items-center+ .pr-2 .fw-700::text").get()
        if pvp.replace('.', '').replace(',', '.').replace('-', '') == '':
            pvp = 0
        else:
            pvp = float(pvp.replace('.', '').replace(',', '.'))

        evEbitida = response.css(
            ".item:nth-child(5) .align-items-center+ .pr-2 .fw-700::text").get()
        evEbit = response.css(
            ".w-100:nth-child(1) .item:nth-child(6) .fw-700::text").get()
        pEbitida = response.css(".item:nth-child(7) .fw-700::text").get()
        pEbit = response.css(".item:nth-child(8) .fw-700::text").get()
        vpa = response.css('.item:nth-child(9) .fw-700::text').get()
        if vpa.replace('.', '').replace(',', '.').replace('-', '') == '':
            vpa = 0
        else:
            vpa = float(vpa.replace('.', '').replace(',', '.'))

        pativo = response.css('.item:nth-child(10) .fw-700::text').get()
        lpa = response.css('.item:nth-child(11) .fw-700::text').get()
        if lpa.replace('.', '').replace(',', '.').replace('-', '') == '':
            lpa = 0
        else:
            lpa = float(lpa.replace('.', '').replace(',', '.'))

        psr = response.css('.item:nth-child(12) .fw-700::text').get()
        pCapGiro = response.css('.item:nth-child(13) .fw-700::text').get()
        pAtivoCircLiq = response.css('.item:nth-child(14) .fw-700::text').get()
        divLiquidaPl = response.css(
            '.w-lg-16_6:nth-child(1) .align-items-center+ .pr-2 .fw-700::text').get()
        divLiquidaEbitida = response.css(
            '.w-100+ .w-100 .w-lg-16_6:nth-child(2) .fw-700::text').get()
        divLiquidaEbit = response.css(
            '.w-lg-16_6:nth-child(3) .align-items-center+ .pr-2 .fw-700::text').get()
        plAtivo = response.css(
            '.w-lg-16_6:nth-child(4) .uppercase+ .pr-2 .fw-700::text').get()
        passivoAtivo = response.css(
            '.item:nth-child(5) .uppercase+ .pr-2 .fw-700::text').get()
        liqCorrente = response.css(
            '.w-100+ .w-100 .item:nth-child(6) .fw-700::text').get()
        mBruta = response.css(
            '.w-lg-33:nth-child(3) .item:nth-child(1) .fw-700::text').get()
        mEbitda = response.css(
            '.w-lg-33:nth-child(3) .item:nth-child(2) .fw-700::text').get()
        mEbit = response.css(
            '.w-lg-33:nth-child(3) .item:nth-child(3) .fw-700::text').get()
        mliquida = response.css(
            '.w-lg-50:nth-child(4) .align-items-center+ .pr-2 .fw-700::text').get()
        roe = response.css(
            '.w-lg-33+ .w-lg-33 .item:nth-child(1) .align-items-center+ .pr-2 .fw-700::text').get()
        roa = response.css(
            '.w-lg-33+ .w-lg-33 .item:nth-child(2) .align-items-center+ .pr-2 .fw-700::text').get()
        roic = response.css(
            '.w-lg-33+ .w-lg-33 .item~ .item+ .item .align-items-center+ .pr-2 .fw-700::text').get()
        giroAtivos = response.css(
            '.item~ .item+ .w-lg-50 .uppercase+ .pr-2 .fw-700::text').get()
        cagrReceitasCincoAnos = response.css(
            '.w-lg-50:nth-child(1) .uppercase+ .pr-2 .fw-700::text').get()
        cagrLucrosCincoAnos = response.css(
            '.w-lg-33~ .w-lg-33+ .w-lg-33 .item+ .item .fw-700::text').get()

        items['indice'] = indice
        items['ticker'] = ticker
        items['empresa'] = empresa
        items['valorAtual'] = valorAtual

        if minCiquentaDuaSemana.replace(',', '.').replace('-', '') == '':
            items['minCiquentaDuaSemana'] = 0
        else:
            items['minCiquentaDuaSemana'] = float(
                minCiquentaDuaSemana.replace(',', '.'))

        if maxCiquentaDuaSemana.replace(',', '.').replace('-', '') == '':
            items['maxCiquentaDuaSemana'] = 0
        else:
            items['maxCiquentaDuaSemana'] = float(
                maxCiquentaDuaSemana.replace(',', '.'))

        if minMes.replace('R$ -', '') == '':
            items['minMes'] = 'R$ 0,00'
        else:
            items['minMes'] = minMes

        if maxMes.replace('R$ -', '') == '':
            items['maxMes'] = 'R$ 0,00'
        else:
            items['maxMes'] = maxMes

        items['valorizacaoBaseDiaAnterior'] = valorizacaoBaseDiaAnterior

        if dy.replace(',', '.').replace('-', '') == '':
            items['dy'] = 0
        else:
            items['dy'] = float(dy.replace(',', '.'))
        items['somaDyDozeMeses'] = somaDyDozeMeses

        if valorizacaoAtivoDozeMeses.replace('-%', '') == '':
            items['valorizacaoAtivoDozeMeses'] = '0,00%'
        else:
            items['valorizacaoAtivoDozeMeses'] = valorizacaoAtivoDozeMeses

        if valorizacaoMesAtual.replace('-%', '') == '':
            items['valorizacaoMesAtual'] = '0,00%'
        else:
            items['valorizacaoMesAtual'] = valorizacaoMesAtual

        items['tipoAtivo'] = tipoAtivo

        items['pl'] = pl

        if pegRatio.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['pegRatio'] = 0
        else:
            items['pegRatio'] = float(
                pegRatio.replace('.', '').replace(',', '.'))

        items['pvp'] = pvp

        if evEbitida.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['evEbitida'] = 0
        else:
            items['evEbitida'] = float(
                evEbitida.replace('.', '').replace(',', '.'))

        if evEbit.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['evEbit'] = 0
        else:
            items['evEbit'] = float(evEbit.replace('.', '').replace(',', '.'))

        if pEbitida.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['pEbitida'] = 0
        else:
            items['pEbitida'] = float(
                pEbitida.replace('.', '').replace(',', '.'))

        if pEbit.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['pEbit'] = 0
        else:
            items['pEbit'] = float(pEbit.replace('.', '').replace(',', '.'))

        items['vpa'] = vpa

        if pativo.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['pativo'] = 0
        else:
            items['pativo'] = float(pativo.replace('.', '').replace(',', '.'))

        items['lpa'] = lpa

        if psr.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['psr'] = 0
        else:
            items['psr'] = float(psr.replace('.', '').replace(',', '.'))

        if pCapGiro.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['pCapGiro'] = 0
        else:
            items['pCapGiro'] = float(
                pCapGiro.replace('.', '').replace(',', '.'))

        if pAtivoCircLiq.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['pAtivoCircLiq'] = 0
        else:
            items['pAtivoCircLiq'] = float(
                pAtivoCircLiq.replace('.', '').replace(',', '.'))

        if divLiquidaPl.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['divLiquidaPl'] = 0
        else:
            items['divLiquidaPl'] = float(
                divLiquidaPl.replace('.', '').replace(',', '.'))

        if divLiquidaEbitida.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['divLiquidaEbitida'] = 0
        else:
            items['divLiquidaEbitida'] = float(
                divLiquidaEbitida.replace('.', '').replace(',', '.'))

        if divLiquidaEbit.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['divLiquidaEbit'] = 0
        else:
            items['divLiquidaEbit'] = float(
                divLiquidaEbit.replace('.', '').replace(',', '.'))

        if plAtivo.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['plAtivo'] = 0
        else:
            items['plAtivo'] = float(
                plAtivo.replace('.', '').replace(',', '.'))

        if passivoAtivo.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['passivoAtivo'] = 0
        else:
            items['passivoAtivo'] = float(
                passivoAtivo.replace('.', '').replace(',', '.'))

        if liqCorrente.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['liqCorrente'] = 0
        else:
            items['liqCorrente'] = float(
                liqCorrente.replace('.', '').replace(',', '.'))

        if mBruta.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['mBruta'] = 0
        else:
            items['mBruta'] = float(mBruta.replace(
                '.', '').replace(',', '.').replace('%', ''))

        if mEbitda.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['mEbitda'] = 0
        else:
            items['mEbitda'] = float(mEbitda.replace(
                '.', '').replace(',', '.').replace('%', ''))

        if mEbit.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['mEbit'] = 0
        else:
            items['mEbit'] = float(mEbit.replace(
                '.', '').replace(',', '.').replace('%', ''))

        if mliquida.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['mliquida'] = 0
        else:
            items['mliquida'] = float(mliquida.replace(
                '.', '').replace(',', '.').replace('%', ''))

        if roe.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['roe'] = 0
        else:
            items['roe'] = float(roe.replace(
                '.', '').replace(',', '.').replace('%', ''))

        if roa.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['roa'] = 0
        else:
            items['roa'] = float(roa.replace(
                '.', '').replace(',', '.').replace('%', ''))

        if roic.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['roic'] = 0
        else:
            items['roic'] = float(roic.replace(
                '.', '').replace(',', '.').replace('%', ''))

        if giroAtivos.replace('.', '').replace(',', '.').replace('-', '') == '':
            items['giroAtivos'] = 0
        else:
            items['giroAtivos'] = float(
                giroAtivos.replace('.', '').replace(',', '.'))

        if cagrReceitasCincoAnos.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['cagrReceitasCincoAnos'] = 0
        else:
            items['cagrReceitasCincoAnos'] = float(
                cagrReceitasCincoAnos.replace('.', '').replace(',', '.').replace('%', ''))

        if cagrLucrosCincoAnos.replace('.', '').replace(',', '.').replace('-', '').replace('%', '') == '':
            items['cagrLucrosCincoAnos'] = 0
        else:
            items['cagrLucrosCincoAnos'] = float(cagrLucrosCincoAnos.replace(
                '.', '').replace(',', '.').replace('%', ''))

        valorIntriseco = sqrt((pl*pvp)*lpa*vpa)
        margemSeguranca = valorIntriseco - valorAtual
        items['valorIntriseco'] = valorIntriseco
        items['margemSeguranca'] = margemSeguranca
        items['setorBtres'] = setorBtres

        yield items
