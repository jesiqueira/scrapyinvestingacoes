# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StatusItem(scrapy.Item):
    # define the fields for your item here like:
    ticker = scrapy.Field()
    valorAtual = scrapy.Field()
    minCiquentaDuaSemana = scrapy.Field()
    maxCiquentaDuaSemana = scrapy.Field()
    minMes = scrapy.Field()
    maxMes = scrapy.Field()
    valorizacaoBaseDiaAnterior = scrapy.Field()
    dy = scrapy.Field()
    somaDyDozeMeses = scrapy.Field()
    valorizacaoAtivoDozeMeses = scrapy.Field()
    valorizacaoMesAtual = scrapy.Field()
    tipoAtivo = scrapy.Field()
    pl = scrapy.Field()
    pegRatio = scrapy.Field()
    pvp = scrapy.Field()
    evEbitida = scrapy.Field()
    evEbit = scrapy.Field()
    pEbitida = scrapy.Field()
    pEbit = scrapy.Field()
    vpa = scrapy.Field()
    pativo = scrapy.Field()
    lpa = scrapy.Field()
    psr = scrapy.Field()
    pCapGiro = scrapy.Field()
    pAtivoCircLiq = scrapy.Field()
    divLiquidaPl = scrapy.Field()
    divLiquidaEbitida = scrapy.Field()
    divLiquidaEbit = scrapy.Field()
    plAtivo = scrapy.Field()
    passivoAtivo = scrapy.Field()
    liqCorrente = scrapy.Field()
    mBruta = scrapy.Field()
    mEbitda = scrapy.Field()
    mEbit = scrapy.Field()
    mliquida = scrapy.Field()
    roe = scrapy.Field()
    roa = scrapy.Field()
    roic = scrapy.Field()
    giroAtivos = scrapy.Field()
    cagrReceitasCincoAnos = scrapy.Field()
    cagrLucrosCincoAnos = scrapy.Field()
