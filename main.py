import curses
from tradingview_ta import TA_Handler, Interval
import time

def calcular_variacao_percentual(preco_antigo, preco_novo):
    if preco_antigo == 0:
        return 0
    return ((preco_novo - preco_antigo) / preco_antigo) * 100

# Defina os tickers das criptos
cryptos = ['BTCUSD', 'SOLUSD', 'XRPUSD']

def obter_dados(crypto):
    handler = TA_Handler(
        symbol=crypto,
        exchange="BINANCE",
        screener="crypto",
        interval=Interval.INTERVAL_1_MINUTE
    )
    analysis = handler.get_analysis().indicators
    return analysis['close'], analysis['volume']

def main(stdscr):
    try:
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)

        precos_iniciais = {crypto: obter_dados(crypto) for crypto in cryptos}
        precos_anteriores = precos_iniciais.copy()
        curses.curs_set(0)  # Esconder el cursor
        stdscr.nodelay(1)  # No bloquear en getch()
        stdscr.timeout(30000)  # Actualizar cada 30000 ms (30 segundos)

        linha = 0
        while True:
            precos_novos = {crypto: obter_dados(crypto) for crypto in cryptos}
            stdscr.clear()
            for i, crypto in enumerate(cryptos):
                preco_inicial, volume_inicial = precos_iniciais[crypto]
                preco_novo, volume_novo = precos_novos[crypto]
                preco_antigo, volume_antigo = precos_anteriores[crypto]
                variacao_preco = calcular_variacao_percentual(preco_antigo, preco_novo)
                variacao_volume = calcular_variacao_percentual(volume_antigo, volume_novo)

                try:
                    stdscr.addstr(linha, 0, f'{crypto}:', curses.color_pair(1))
                    stdscr.addstr(linha + 1, 0, f'  Preço Inicial: {preco_inicial:.2f}', curses.color_pair(2))
                    stdscr.addstr(linha + 2, 0, f'  Preço Atual: {preco_novo:.2f}', curses.color_pair(2))
                    stdscr.addstr(linha + 3, 0, f'  Variação Preço: {variacao_preco:.2f}%', curses.color_pair(3))
                    stdscr.addstr(linha + 4, 0, f'  Variação Volume: {variacao_volume:.2f}%', curses.color_pair(3))
                except curses.error:
                    pass  # Ignore errors caused by writing outside the window

                linha += 6

            stdscr.refresh()
            precos_anteriores = precos_novos
            linha = 0

            if stdscr.getch() != -1:
                break
    except KeyboardInterrupt:
        pass  # Permitir salir con Ctrl+C sin errores

curses.wrapper(main)