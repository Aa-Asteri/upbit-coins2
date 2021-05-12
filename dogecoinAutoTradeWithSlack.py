import time
import pyupbit
import datetime
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

access = "I2UxPw29ixxiw4yKUguS4dtcfvBYPnkIKi1Tmw7D"
secret = "F8RNFqykSjT0JruTDXIFw5LTHGsOf2s47tdHzNaA"

bot = commands.Bot(command_prefix='!')

@bot.command(name='bot')
async def nine_nine(ctx):

    def get_target_price(ticker, k):
        """변동성 돌파 전략으로 매수 목표가 조회"""
        df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
        target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
        return target_price

    def get_start_time(ticker):
        """시작 시간 조회"""
        df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
        start_time = df.index[0]
        return start_time

    def get_ma15(ticker):
        """15일 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
        ma15 = df['close'].rolling(15).mean().iloc[-1]
        return ma15

    def get_balance(coin):
        """잔고 조회"""
        balances = upbit.get_balances()
        for b in balances:
            if b['currency'] == coin:
                if b['balance'] is not None:
                    return float(b['balance'])
                else:
                    return 0

    def get_current_price(ticker):
        """현재가 조회"""
        return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

    # 로그인
    upbit = pyupbit.Upbit(access, secret)
    print("autotrade start")
    # 시작 메세지 슬랙 전송
    await ctx.send("AutoTrade start")

    while True:
        try:
            now = datetime.datetime.now()
            start_time = get_start_time("KRW-DOGE")
            end_time = start_time + datetime.timedelta(days=1)

            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price("KRW-DOGE", 0.7)
                ma15 = get_ma15("KRW-DOGE")
                current_price = get_current_price("KRW-DOGE")
                if target_price < current_price and ma15 < current_price:
                    krw = get_balance("KRW")
                    if krw > 100:
                        buy_result = upbit.buy_market_order("KRW-DOGE", krw*0.9995)
                        await ctx.send("DOGE buy : " +str(buy_result))
            else:
                doge = get_balance("DOGE")
                if doge > 10:
                    sell_result = upbit.sell_market_order("KRW-DOGE", doge*0.9995)
                    await ctx.send("DOGE sell : " +str(sell_result))
            time.sleep(1)
        except Exception as e:
            print(e)
            await ctx.send(e)
            time.sleep(1)
bot.run(TOKEN)
