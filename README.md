# Data Crawling API server

## Description

1. 미국, 인도, 중국(홍콩)의 거래소에서 필요한 data들을 크롤링한다.
2. 크롤링 스크립트를 만들고 이를 바탕으로 DB에 저장한다.
3. DB에 있는 Data를 바탕으로 포트폴리오를 작성할 수 있는 코드를 만든다.
4. 이를 Flask api를 이용해 WAS의 api 명세서에 맞춘 JSON 형태로 WAS 서버로 보낸다.
5. 이 행위들은 자동화되어야한다.

## API 요구사항

### company_data (분기마다 자동 update)

- per
- pbr
- roa
- roe
- debt_ratio(부채비율)
- operating_profit_ratio(영업이익률)
- reserve_ratio(유보율)

### company_detail (분기마다 자동 update)

- code(종목코드)
- cmp_name(종목명/기업이름)
- total_asset(총자산)
- total_equity(총자본)
- total_debt(총부채)
- sales(매출액)
- operating_profit(영업이익)
- net_income(당기손이익)
- retained_earnings(이익 잉여금)
- description(기업상세설명)
- market(업종)

### daily_price (매일 장마감 기준으로 자동 update)

- code(종목코드)
- end_price(종가)

## 10월 5일

1. 스크립트를 짜서 각 나라별로 데이터를 뽑아보려고 했으나, 상당히 많은 양의 데이터로 인해 시간이 꽤나 걸릴것으로 추정됨.
2. 만약, 인터넷 문제가 아니라, 말그대로 데이터가 매우 많아 그런것이라면, api 요구 사항에 맞는 데이터들만 뽑거나, 미국의 top 10 기업들의 포트폴리오를 뽑아내는 방식으로 해야할듯
