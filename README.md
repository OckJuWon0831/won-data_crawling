# Data Crawling API server

## Description

1. 미국, 인도, 중국(홍콩)의 거래소에서 필요한 data들을 크롤링한다.
2. WAS(Spring boot)에서 요구하는 api 명세서에 맞게 처리 후, json 형태로 보내준다.
3. 파이썬 코드를 실행하는 Scheduling은 WAS의 환경설정에 맞춰 AWS 환경내에서 설정한다.

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
