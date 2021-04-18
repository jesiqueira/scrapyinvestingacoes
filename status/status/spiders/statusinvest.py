import scrapy
import json
from ..items import StatusItem
from ..config import API

from scraper_api import ScraperAPIClient
client = ScraperAPIClient(API)


class StatusinvestSpider(scrapy.Spider):
    name = 'statusinvest'
    start_urls = [
        client.scrapyGet('https://statusinvest.com.br/acoes/busca-avancada')
    ]

    def parse(self, response):
        url = "https://statusinvest.com.br/category/advancedsearchresult?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%220%3B25%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22peg_Ratio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22vpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorMercado%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=1"

        yield scrapy.Request(url, callback=self.parse_api)

    def parse_api(self, response):
        base_url = "https://statusinvest.com.br/acoes/"
        raw_data = response.body
        data = json.loads(raw_data)

        for status in data:
            papel = status['ticker']
            status_url = base_url+papel
            yield scrapy.Request(client.scrapyGet(status_url), callback=self.parse_status)

    def parse_status(self, response):
        items = StatusItem()
        ticker = response.css(".fw-900.active::text").get()
        valorAtual = response.css('.value::text').get()
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
        pegRatio = response.css(
            ".item:nth-child(3) .uppercase+ .pr-2 .fw-700::text").get()
        pvp = response.css(
            ".w-lg-16_6:nth-child(4) .align-items-center+ .pr-2 .fw-700::text").get()
        evEbitida = response.css(
            ".item:nth-child(5) .align-items-center+ .pr-2 .fw-700::text").get()
        evEbit = response.css(
            ".w-100:nth-child(1) .item:nth-child(6) .fw-700::text").get()
        pEbitida = response.css(".item:nth-child(7) .fw-700::text").get()
        pEbit = response.css(".item:nth-child(8) .fw-700::text").get()
        vpa = response.css('.item:nth-child(9) .fw-700::text').get()
        pativo = response.css('.item:nth-child(10) .fw-700::text').get()
        lpa = response.css('.item:nth-child(11) .fw-700::text').get()
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

        items['ticker'] = ticker
        items['valorAtual'] = valorAtual
        items['minCiquentaDuaSemana'] = minCiquentaDuaSemana
        items['maxCiquentaDuaSemana'] = maxCiquentaDuaSemana
        items['minMes'] = minMes
        items['maxMes'] = maxMes
        items['valorizacaoBaseDiaAnterior'] = valorizacaoBaseDiaAnterior
        items['dy'] = dy
        items['somaDyDozeMeses'] = somaDyDozeMeses
        items['valorizacaoAtivoDozeMeses'] = valorizacaoAtivoDozeMeses
        items['valorizacaoMesAtual'] = valorizacaoMesAtual
        items['tipoAtivo'] = tipoAtivo
        items['pl'] = pl
        items['pegRatio'] = pegRatio
        items['pvp'] = pvp
        items['evEbitida'] = evEbitida
        items['evEbit'] = evEbit
        items['pEbitida'] = pEbitida
        items['pEbit'] = pEbit
        items['vpa'] = vpa
        items['pativo'] = pativo
        items['lpa'] = lpa
        items['psr'] = psr
        items['pCapGiro'] = pCapGiro
        items['pAtivoCircLiq'] = pAtivoCircLiq
        items['divLiquidaPl'] = divLiquidaPl
        items['divLiquidaEbitida'] = divLiquidaEbitida
        items['divLiquidaEbit'] = divLiquidaEbit
        items['plAtivo'] = plAtivo
        items['passivoAtivo'] = passivoAtivo
        items['liqCorrente'] = liqCorrente
        items['mBruta'] = mBruta
        items['mEbitda'] = mEbitda
        items['mEbit'] = mEbit
        items['mliquida'] = mliquida
        items['roe'] = roe
        items['roa'] = roa
        items['roic'] = roic
        items['giroAtivos'] = giroAtivos
        items['cagrReceitasCincoAnos'] = cagrReceitasCincoAnos
        items['cagrLucrosCincoAnos'] = cagrLucrosCincoAnos

        yield items
